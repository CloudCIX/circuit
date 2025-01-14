"""
Management of Property Value
"""
# libs
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.models import Q
# local
from circuit.models import Circuit
from circuit.utils import get_addresses_in_member


__all__ = [
    'PropertyValueCollection',
]


class PropertyValueCollection(APIView):
    """
    Handles methods regarding Property_value records that don't require an id to be specified
    """

    def get(self, request: Request, search_term: str) -> Response:
        """
        summary: Retrieve a list of Circuit Properties filtered by sent search_term value.

        description: |
            Retrieve a list of Circuit Properties that contain sent search_term for the requesting User's Address.

            The data is returned in a map similar to
            ```
            {
              circuit_id: -1,
              property_value: 'search_term',
              reference: 'my circuit',
              reference_number: -1,
            }
            ```

        path_params:
            search_term:
                description: The search_term to filter Circuit Properties by.
                type: string

        responses:
            200:
                description: A list of Circuit Properties that contain the sent search_term
                content:
                    application/json:
                        schema:
                            type: object
        """
        tracer = settings.TRACER

        # Now get a list of Circuit records using the filters
        with tracer.start_span('set_address_filtering', child_of=request.span) as span:
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

        with tracer.start_span('get_objects', child_of=request.span):
            # Apply address filtering
            objs = Circuit.objects.filter(address_filtering, decommission_date__isnull=True)
            # Filtering results by sent search_term
            objs = objs.filter(properties__icontains=search_term)
            results = []
            for circuit in objs:
                for value in circuit.properties.values():
                    value = str(value)
                    if search_term.lower() in value.lower():
                        results.append({
                            'circuit_id': circuit.id,
                            'property_value': value,
                            'reference': circuit.reference,
                            'reference_number': circuit.reference_number,
                        })
            # Sort results alphabetically
            results = sorted(results, key=lambda x: x['property_value'])

        return Response({'content': results}, status=status.HTTP_200_OK)
