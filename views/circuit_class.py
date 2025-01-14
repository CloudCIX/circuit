"""
Management of Circuit Class
"""
# stdlib
from datetime import datetime
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from circuit.controllers import (
    CircuitClassCreateController,
    CircuitClassListController,
    CircuitClassUpdateController,
)
from circuit.models import CircuitClass, Property
from circuit.permissions.circuit_class import Permissions
from circuit.serializers import CircuitClassSerializer


__all__ = [
    'CircuitClassCollection',
    'CircuitClassResource',
]


class CircuitClassCollection(APIView):
    """
    Handles methods regarding circuit class records that don't require an id to be specified
    """

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Circuit Class records

        description: |
            Retrieve a list of Circuit Class records for the requesting User's Member.

        responses:
            200:
                description: A list of Circuit Class records, filtered and ordered by the User.
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CircuitClassListController(data=request.GET, request=request, span=span)
            # By validating the controller we will generate the filters
            controller.is_valid()
        # Now get a list of CircuitClass records using the filters
        with tracer.start_span('get_objects', child_of=request.span):
            try:
                # Search and exclude can be empty dicts so there's no need to check
                # if they're populated
                objs = CircuitClass.objects.filter(
                    member_id=request.user.member['id'],
                    **controller.cleaned_data['search'],
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='circuit_circuit_class_list_001')

        with tracer.start_span('generating_metadata', child_of=request.span):
            total_records = objs.count()
            page = controller.cleaned_data['page']
            order = controller.cleaned_data['order']
            limit = controller.cleaned_data['limit']
            warnings = controller.warnings

            metadata = {
                'page': page,
                'limit': limit,
                'order': order,
                'total_records': total_records,
                'warnings': warnings,
            }
            objs = objs[page * limit:(page + 1) * limit]

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = CircuitClassSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new CircuitClass record

        description: |
            Create a new CircuitClass record in the requesting User's Member, using the data supplied by the User.

        responses:
            201:
                description: CircuitClass record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        # Have Permission checks as early as possible
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CircuitClassCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            # Pop properties from controller.instance to save after Circuit Class is saved
            properties = controller.cleaned_data.pop('properties')
            # Set Required Values and save controller.instance
            controller.instance.member_id = request.user.member['id']
            controller.instance.save()

        with tracer.start_span('saving_properties_object', child_of=request.span):
            # Set Required Values and save validated properties
            for item in properties:
                Property.objects.create(
                    circuit_class=controller.instance,
                    key=item['key'],
                    property_type=item['property_type'],
                    required=item['required'],
                )

        with tracer.start_span('serializing_data', child_of=request.span):
            data = CircuitClassSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class CircuitClassResource(APIView):
    """
    Handles methods regarding circuit class records that do require an id to be specified, i.e. update, delete
    """

    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Circuit Class record

        description: |
            Attempt to read a Circuit Class record by the given `pk`, returning a 404 if it does not exist.

        path_params:
            pk:
                description: The id of the Circuit Class record to be read.
                type: integer

        responses:
            200:
                description: Circuit Class record was read successfully.
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = CircuitClass.objects.get(id=pk, member_id=request.user.member['id'])
            except CircuitClass.DoesNotExist:
                return Http404(error_code='circuit_circuit_class_read_001')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = CircuitClassSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Circuit Class record

        description: |
            Attempt to update a Circuit Class record in the requesting User's Member by the given `pk`,
            returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Circuit Class record to be updated
                type: integer
        responses:
            200:
                description: Circuit Class record was updated successfully
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_department_object', child_of=request.span):
            try:
                obj = CircuitClass.objects.get(id=pk, member_id=request.user.member['id'])
            except CircuitClass.DoesNotExist:
                return Http404(error_code='circuit_circuit_class_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CircuitClassUpdateController(
                instance=obj,
                data=request.data,
                request=request,
                partial=partial,
                span=span,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            properties = controller.cleaned_data.pop('properties')
            controller.instance.save()

        with tracer.start_span('updating_properties_object', child_of=request.span):
            # Set deleted property to current time for existing properties
            obj.properties.all().update(deleted=datetime.now())

            # Create and save new Property objects with updated values
            for item in properties:
                Property.objects.create(
                    circuit_class=controller.instance,
                    key=item['key'],
                    property_type=item['property_type'],
                    required=item['required'],
                )

        with tracer.start_span('serializing_data', child_of=request.span):
            data = CircuitClassSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a circuit class record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int):
        """
        summary: Delete a specified CircuitClass record

        description: |
            Attempt to delete a CircuitClass record in the requesting User's Member by the given `pk`,
            returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the CircuitClass record to delete
                type: integer

        responses:
            204:
                description: CircuitClass record was deleted successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_department_object', child_of=request.span):
            try:
                obj = CircuitClass.objects.get(id=pk, member_id=request.user.member['id'])
            except CircuitClass.DoesNotExist:
                return Http404(error_code='circuit_circuit_class_delete_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.delete(request, obj)
            if err is not None:
                return err

        with tracer.start_span('saving_object', child_of=request.span):
            obj.cascade_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
