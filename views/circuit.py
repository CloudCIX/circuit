"""
Management of Circuit
"""
# stdlib
from datetime import datetime
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db.models import Q
# local
from circuit.controllers.circuit import (
    CircuitCreateController,
    CircuitListController,
    CircuitUpdateController,
)
from circuit.models import Circuit
from circuit.permissions.circuit import Permissions
from circuit.serializers import CircuitSerializer
from circuit.utils import get_addresses_in_member


__all__ = [
    'CircuitCollection',
    'CircuitResource',
]


class CircuitCollection(APIView):
    """
    Handles methods regarding Circuit records that don't require an id to be specified
    """

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Circuit records
        description: |
            Retrieve a list of Circuit records for the requesting User's Member.
        responses:
            200:
                description: A list of Circuit records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CircuitListController(data=request.GET, request=request, span=span)
            # By validating the controller we will generate the filters
            controller.is_valid()
        # Now get a list of Circuit records using the filters
        with tracer.start_span('get_objects', child_of=request.span):
            # A global-active user can list all projects in their member
            if request.user.is_global and request.user.global_active:
                addresses = get_addresses_in_member(request, span)
                address_filtering = (
                    Q(address_id__in=addresses) |
                    Q(customer_address_id__in=addresses) |
                    Q(service_provider_address_id__in=addresses)
                )
            else:
                address_filtering = (
                    Q(address_id=request.user.address['id']) |
                    Q(customer_address_id=request.user.address['id']) |
                    Q(service_provider_address_id=request.user.address['id'])
                )
            try:
                # Search and exclude can be empty dicts so there's no need to check
                # if they're populated
                # Filtering first by what was sent in request
                objs = Circuit.objects.filter(
                    **controller.cleaned_data['search'],
                )
                # Filtering results by address_filtering and then applying exclusions and ordering
                objs = objs.filter(address_filtering).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )

            except (ValueError, ValidationError):
                return Http400(error_code='circuit_circuit_list_001')

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
            data = CircuitSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Circuit record

        description: |
            Create a new Circuit record in the requesting User's Member, using the data supplied by the User.

        responses:
            201:
                description: Circuit record was created successfully
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
            controller = CircuitCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.address_id = request.user.address['id']
            controller.instance.save()
            # Refresh after saving to add refernece_number generated by trigger to response data
            controller.instance.refresh_from_db()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = CircuitSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class CircuitResource(APIView):
    """
    Handles methods regarding Circuit records that do require an id to be specified, i.e. delete, read, update
    """

    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Circuit record

        description: |
            Attempt to read a Circuit record by the given `pk`, returning a 404 if it does not exist.

        path_params:
            pk:
                description: The id of the Circuit record to be read.
                type: integer
        responses:
            200:
                description: Circuit record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_request_object', child_of=request.span):
            try:
                obj = Circuit.objects.get(id=pk)
            except Circuit.DoesNotExist:
                return Http404(error_code='circuit_circuit_read_001')

        # Check perms for the user and object
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, obj, request.span)
            if err is not None:
                return err

        with tracer.start_span('serializing_data', child_of=request.span):
            data = CircuitSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Circuit record
        description: |
            Attempt to update a Circuit record by the given `pk`, returning a 404 if it does not exist.
        path_params:
            pk:
                description: The id of the Circuit record to be updated.
                type: integer
        responses:
            200:
                description: Circuit record was updated successfully
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Circuit.objects.get(id=pk, address_id=request.user.address['id'])
            except Circuit.DoesNotExist:
                return Http404(error_code='circuit_circuit_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CircuitUpdateController(
                instance=obj,
                data=request.data,
                request=request,
                partial=partial,
                span=span,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = CircuitSerializer(instance=controller.instance).data

        return Response({'content': data})

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a Member record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int):
        """
        summary: Delete a specified Circuit record

        description: |
            Attempt to delete a Circuit record in the requesting User's Member by the given `pk`, returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Circuit record to delete
                type: integer

        responses:
            204:
                description: Circuit record was deleted successfully
            404: {}
        """

        tracer = settings.TRACER

        with tracer.start_span('retrieving_request_object', child_of=request.span):
            try:
                obj = Circuit.objects.get(id=pk, address_id=request.user.address['id'])
            except Circuit.DoesNotExist:
                return Http404(error_code='circuit_circuit_delete_001')

        with tracer.start_span('saving_object', child_of=request.span):
            obj.deleted = datetime.now()
            obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
