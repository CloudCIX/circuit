# stdlib
from collections import deque
from typing import Any, Deque, Dict, List, Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from circuit.models import CircuitClass, Property, PropertyType


__all__ = [
    'CircuitClassCreateController',
    'CircuitClassListController',
    'CircuitClassUpdateController',
]


class CircuitClassListController(ControllerBase):
    """
    Validates User data used to filter a list of CircuitClass records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some ControllerBase.Meta fields to make them more
        specific for this Controller
        """

        allowed_ordering = (
            'name',
            'created',
            'id',
            'updated',
        )
        search_fields = {
            'created': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'updated': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }


class CircuitClassCreateController(ControllerBase):
    """
    Validates User data used to create a new CircuitClass record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = CircuitClass
        validation_order = (
            'name',
            'properties',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the CircuitClass
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'circuit_circuit_class_create_101'
        if len(name) > self.get_field('name').max_length:
            return 'circuit_circuit_class_create_102'
        circuit_class = CircuitClass.objects.filter(
            name=name,
            member_id=self.request.user.member['id'],
        )
        if circuit_class.exists():
            return 'circuit_circuit_class_create_103'
        self.cleaned_data['name'] = name
        return None

    def validate_properties(self, properties: Optional[List[Dict[str, Any]]]) -> Optional[str]:
        """
        description: The properties of the CircuitClass
        type: array
        items:
            type: object
            properties:
                key:
                    description: The key name for the property
                    type: string
                property_type_id:
                    description: ID of Property Type record assigned to the Property instance.
                    type: integer
                required:
                    description: A flag stating if the Property Key is rquired when creating a Circuit.
                    type: boolean
        """
        properties = properties or []
        if not isinstance(properties, list):
            return 'circuit_circuit_class_create_104'
        if len(properties) == 0:
            return 'circuit_circuit_class_create_105'
        keys: List[str] = []
        results: Deque = deque()
        for i, item in enumerate(properties):
            if not isinstance(item, dict):
                return 'circuit_circuit_class_create_106'
            property_type_id = item.get('property_type_id', None)
            if property_type_id is None:
                return 'circuit_circuit_class_create_107'
            try:
                property_type = PropertyType.objects.get(id=property_type_id)
            except PropertyType.DoesNotExist:
                return 'circuit_circuit_class_create_108'
            key = item.get('key', None)
            if key is None:
                return 'circuit_circuit_class_create_109'
            if len(key) > Property._meta.get_field('key').max_length:
                return 'circuit_circuit_class_create_110'
            if key in keys:
                return 'circuit_circuit_class_create_111'
            keys.append(key)
            required = item.get('required', None)
            if required is None:
                return 'circuit_circuit_class_create_112'
            if not isinstance(required, bool):
                return 'circuit_circuit_class_create_113'
            results.append({
                'property_type': property_type,
                'key': key,
                'required': required,
            })
        self.cleaned_data['properties'] = results
        return None


class CircuitClassUpdateController(ControllerBase):
    """
    Validates User data used to update a CircuitClass record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = CircuitClass
        validation_order = (
            'name',
            'properties',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the CircuitClass
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'circuit_circuit_class_update_101'
        if len(name) > self.get_field('name').max_length:
            return 'circuit_circuit_class_update_102'
        circuit_class = CircuitClass.objects.filter(
            name=name,
            member_id=self.request.user.member['id'],
        ).exclude(
            pk=self._instance.pk,
        )
        if circuit_class.exists():
            return 'circuit_circuit_class_update_103'
        self.cleaned_data['name'] = name
        return None

    def validate_properties(self, properties: Optional[List[Dict[str, Any]]]) -> Optional[str]:
        """
        description: The properties of the CircuitClass
        type: array#
        items:
            type: object
            properties:
                key:
                    description: The key name for the property
                    type: string
                property_type_id:
                    description: ID of Property Type record assigned to the Property instance.
                    type: integer
                required:
                    description: A flag stating if the Property Key is rquired when creating a Circuit.
                    type: boolean
        """
        properties = properties or []
        if not isinstance(properties, list):
            return 'circuit_circuit_class_update_104'
        if len(properties) == 0:
            return 'circuit_circuit_class_update_105'
        keys: List[str] = []

        if self._instance.total_circuits > 0:
            current_properties = {o.key: o.property_type.pk for o in self._instance.properties.filter(
                deleted__isnull=True,
            )}
            for key in current_properties:
                if not any(prop.get('key') == key for prop in properties):
                    return 'circuit_circuit_class_update_106'

        results: Deque = deque()
        for item in properties:
            if not isinstance(item, dict):
                return 'circuit_circuit_class_update_107'
            property_type_id = item.get('property_type_id', None)
            if property_type_id is None:
                return 'circuit_circuit_class_update_108'
            try:
                property_type = PropertyType.objects.get(id=property_type_id)
            except PropertyType.DoesNotExist:
                return 'circuit_circuit_class_update_109'
            key = item.get('key', None)
            if key is None:
                return 'circuit_circuit_class_update_110'
            if len(key) > Property._meta.get_field('key').max_length:
                return 'circuit_circuit_class_update_111'
            if key in keys:
                return 'circuit_circuit_class_update_112'
            keys.append(key)
            required = item.get('required', None)
            if required is None:
                return 'circuit_circuit_class_update_113'
            if not isinstance(required, bool):
                return 'circuit_circuit_class_update_114'

            results.append({
                'property_type': property_type,
                'key': key,
                'required': required,
            })
        self.cleaned_data['properties'] = results
        return None
