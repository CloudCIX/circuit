"""
Management of Property Type
"""
# libs
from cloudcix_rest.exceptions import Http400
from cloudcix_rest.views import APIView
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
# local
from circuit.controllers import PropertyTypeListController
from circuit.models import PropertyType
from circuit.serializers import PropertyTypeSerializer


__all__ = [
    'PropertyTypeCollection',
]


class PropertyTypeCollection(APIView):
    """
    Handles methods regarding Property type records that don't require an id to be specified
    """

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Property type records

        description: |
            Retrieve a list of Property Type records for the requesting User's Member.

        responses:
            200:
                description: A list of Property Type records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = PropertyTypeListController(data=request.GET, request=request, span=span)
            # By validating the controller we will generate the filters
            controller.is_valid()
        # Now get a list of PropertyType records using the filters
        with tracer.start_span('get_objects', child_of=request.span):
            try:
                # Search and exclude can be empty dicts so there's no need to check
                # if they're populated
                objs = PropertyType.objects.filter(
                    **controller.cleaned_data['search'],
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='circuit_property_type_list_001')

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
            data = PropertyTypeSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})
