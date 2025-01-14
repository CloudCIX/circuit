"""
Permissions classes will use their methods to validate permissions for a
request.
These methods will raise any errors that may occur so all you have to do is
call the method in the view
"""
# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from opentracing.span import Span
from rest_framework.request import Request
# local
from circuit.models import Circuit
from circuit.utils import get_addresses_in_member

__all__ = [
    'Permissions',
]


class Permissions:

    @staticmethod
    def create(request: Request) -> Optional[Http403]:
        """
        The request to create a new Circuit record is valid if:
        - The requesting User's Member is self-managed
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='circuit_circuit_create_201')
        return None

    @staticmethod
    def read(request: Request, obj: Circuit, span: Span) -> Optional[Http403]:
        """
        The request to read a Circuit is valid if;
        - The requesting User address is the address_id, customer_address_id or service_provider_address_id
        - The requesting User is global and one of the addresses is in their Member
        customer_address_id or service_provider_address_id of the object
        """
        # The requesting User address is the address_id, customer_address_id or service_provider_address_id
        if request.user.address['id'] not in [obj.address_id, obj.customer_address_id, obj.service_provider_address_id]:
            # The requesting User is global and one of the addresses is in their Member
            if request.user.is_global and request.user.global_active:
                addresses = get_addresses_in_member(request, span)
                if not any([True for e in (
                        obj.address_id,
                        obj.customer_address_id,
                        obj.service_provider_address_id,
                ) if e in addresses]):
                    return Http403(error_code='circuit_circuit_read_201')
            else:
                return Http403(error_code='circuit_circuit_read_202')

        return None
