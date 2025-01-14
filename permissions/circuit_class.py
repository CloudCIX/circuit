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
from rest_framework.request import Request
# local
from circuit.models import CircuitClass, Circuit


class Permissions:

    @staticmethod
    def create(request: Request) -> Optional[Http403]:
        """
        The request to create a new Circuit Class record is valid if:
        - The requesting User's Member is self-managed
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='circuit_circuit_class_create_201')
        return None

    @staticmethod
    def delete(request: Request, obj: CircuitClass) -> Optional[Http403]:
        """
        The request to delete a Circuit Class record is valid if:
        - There are no Circuits asssociated with the Circuit Class
        """
        # There are no Circuits associated with the Circuit Class
        if Circuit.objects.filter(circuit_class=obj, deleted__isnull=True).exists():
            return Http403(error_code='circuit_circuit_class_delete_201')
        return None
