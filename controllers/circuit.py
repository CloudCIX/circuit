
# stdlib
from decimal import Decimal
from typing import Any, Dict, Optional

# libs
from cloudcix.api.membership import Membership
from cloudcix_rest.controllers import ControllerBase
from dateutil import parser
from netaddr import AddrFormatError, IPNetwork
from urllib.parse import urlparse

# local
from circuit.models import Circuit, CircuitClass

__all__ = [

    'CircuitListController',
    'CircuitCreateController',
    'CircuitUpdateController',
]


class CircuitListController(ControllerBase):
    """
    Validates User data used to filter a list of Circuit records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some ControllerBase.Meta fields to make them more
        specific for this Controller
        """
        allowed_ordering = (
            'reference_number',
            'address_id',
            'circuit_class_id',
            'circuit_class__name',
            'created',
            'customer_address_id',
            'decommission_date',
            'description',
            'group_name',
            'id',
            'install_date',
            'reference',
            'service_provider_address_id',
            'updated',
        )
        search_fields = {
            'address_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'circuit_class_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'circuit_class__name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'created': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'customer_address_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'decommission_date': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'description': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'group_name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'install_date': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'reference': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'reference_number': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'service_provider_address_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'updated': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }


class CircuitCreateController(ControllerBase):
    """
    Validates User data used to filter a list of Circuit records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some ControllerBase.Meta fields to make them more
        specific for this Controller
        """

        model = Circuit
        validation_order = (
            'bandwidth',
            'circuit_class_id',
            'customer_address_id',
            'description',
            'group_name',
            'hand_off_point',
            'install_date',
            'decommission_date',
            'properties',
            'reference',
            'service_provider_address_id',
        )

    def validate_bandwidth(self, bandwidth: Optional[int]) -> Optional[str]:
        """
        description: The bandwidth of the Circuit
        required: false
        type: integer
        """
        if bandwidth is None:
            return None

        try:
            bandwidth = int(bandwidth)
        except (ValueError, TypeError):
            return 'circuit_circuit_create_101'

        self.cleaned_data['bandwidth'] = bandwidth
        return None

    def validate_circuit_class_id(self, circuit_class_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Circuit Class
        type: integer
        """
        if circuit_class_id is None:
            return 'circuit_circuit_create_102'

        try:
            circuit_class_id = int(circuit_class_id)
        except (ValueError, TypeError):
            return 'circuit_circuit_create_103'

        try:
            obj = CircuitClass.objects.get(pk=circuit_class_id, member_id=self.request.user.member['id'])
        except CircuitClass.DoesNotExist:
            return 'circuit_circuit_create_104'

        self.cleaned_data['circuit_class'] = obj
        return None

    def validate_customer_address_id(self, customer_address_id: Optional[int]) -> Optional[str]:
        """
        description: The Address ID of the customer for the Circuit
        required: false
        type: integer
        """
        if not(customer_address_id):
            return None

        try:
            customer_address_id = int(customer_address_id)
        except (ValueError, TypeError):
            return 'circuit_circuit_create_106'

        if self.request.user.address['id'] != customer_address_id:
            response = Membership.address.read(
                token=self.request.user.token,
                pk=customer_address_id,
                span=self.span,
            )
            if response.status_code != 200:
                return 'circuit_circuit_create_107'
        self.cleaned_data['customer_address_id'] = customer_address_id
        return None

    def validate_description(self, description: Optional[str]) -> Optional[str]:
        """
        description: A description of the circuit.
        required: false
        type: string
        """
        self.cleaned_data['description'] = str(description)
        return None

    def validate_group_name(self, group_name: Optional[str]) -> Optional[str]:
        """
        description: The group name of the circuit
        required: false
        type: string
        """
        if group_name is None:
            group_name = ''
        group_name = str(group_name).strip()
        if len(group_name) > self.get_field('group_name').max_length:
            return 'circuit_circuit_create_123'
        self.cleaned_data['group_name'] = group_name
        return None

    def validate_hand_off_point(self, hand_off_point: Optional[str]) -> Optional[str]:
        """
        description: The hand off point location for the circuit
        required: false
        type: string
        """
        if hand_off_point is None:
            hand_off_point = ''
        hand_off_point = str(hand_off_point).strip()
        if len(hand_off_point) > self.get_field('hand_off_point').max_length:
            return 'circuit_circuit_create_108'
        self.cleaned_data['hand_off_point'] = hand_off_point
        return None

    def validate_install_date(self, install_date) -> Optional[str]:
        """
        description: Date Circuit was installed
        type: string
        """
        if install_date is None:
            return 'circuit_circuit_create_109'

        try:
            install_date = parser.parse(install_date)
        except(ValueError, TypeError):
            return 'circuit_circuit_create_110'

        self.cleaned_data['install_date'] = install_date
        return None

    def validate_decommission_date(self, decommission_date) -> Optional[str]:
        """
        description: Date Circuit was decommissioned
        required: false
        type: string
        """
        if decommission_date is None:
            return None

        try:
            decommission_date = parser.parse(decommission_date)
        except(ValueError, TypeError):
            return 'circuit_circuit_create_111'

        if 'install_date' not in self.cleaned_data:
            return None
        # Check that it's valid compared to the start_date
        if decommission_date < self.cleaned_data['install_date']:
            return 'circuit_circuit_create_112'

        self.cleaned_data['decommission_date'] = decommission_date
        return None

    def validate_properties(self, properties: Optional[Dict[str, Any]]) -> Optional[str]:
        """
        description: |
            Properties is a dictionary of the property types associated with the assigned circuit class.
            If the Circuit Class has a property with required as True, then it must be included in the request.
            e.g. Circuit Class has "height-cm" and "width-cm" as properties and required is True for "height"
                {
                    'height-cm': 25,
                }
            This will pass because the "width-cm" is not required.
        type: dict
        """
        if 'circuit_class' not in self.cleaned_data:
            # An error was raised for circuit class and cannot proceed with
            # validating properties until resolved
            return None
        circuit_class = self.cleaned_data['circuit_class']
        if circuit_class.properties.count() == 0:
            # Circuit Class has no properties
            return None

        if properties is None:
            # properties are required in case there is a property for the circuit class that is required.
            properties = {}
        if not isinstance(properties, dict):
            return 'circuit_circuit_create_113'
        for p in circuit_class.properties.all():
            if p.key in properties:
                if p.required:
                    if properties.get(p.key) is None:
                        return 'circuit_circuit_create_114'
                value = properties.get(p.key)
                if value:
                    if p.property_type_id == 1:
                        value = str(value)
                    elif p.property_type_id == 2:
                        if not isinstance(value, (int, float, complex, Decimal)):
                            return 'circuit_circuit_create_115'
                    elif p.property_type_id == 3:
                        if not isinstance(value, bool):
                            return None
                    elif p.property_type_id == 4:
                        result = urlparse(value)
                        if not all([result.scheme, result.netloc]):
                            return 'circuit_circuit_create_116'
                    elif p.property_type_id == 5:
                        try:
                            IPNetwork(value)
                        except (TypeError, ValueError, AddrFormatError):
                            return 'circuit_circuit_create_117'
            else:
                if p.required:
                    return 'circuit_circuit_create_118'
                properties.update({p.key: None})

        self.cleaned_data['properties'] = properties
        return None

    def validate_reference(self, reference: Optional[str]) -> Optional[str]:
        """
        description: The reference for this Circuit
        required: false
        type: string
        """
        if reference is None:
            reference = ''
        reference = str(reference).strip()
        if len(reference) > self.get_field('reference').max_length:
            return 'circuit_circuit_create_119'
        self.cleaned_data['reference'] = reference
        return None

    def validate_service_provider_address_id(self, service_provider_address_id: Optional[int]) -> Optional[str]:
        """
        description: The Address ID of the service_provider for the Circuit
        type: integer
        """
        if not(service_provider_address_id):
            return None

        try:
            service_provider_address_id = int(service_provider_address_id)
        except (ValueError, TypeError):
            return 'circuit_circuit_create_121'

        if self.request.user.address['id'] != service_provider_address_id:
            response = Membership.address.read(
                token=self.request.user.token,
                pk=service_provider_address_id,
                span=self.span,
            )
            if response.status_code != 200:
                return 'circuit_circuit_create_122'

        self.cleaned_data['service_provider_address_id'] = service_provider_address_id
        return None


class CircuitUpdateController(ControllerBase):
    """
    Validates User data used to filter a list of Circuit records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some ControllerBase.Meta fields to make them more
        specific for this Controller
        """

        model = Circuit
        validation_order = (
            'bandwidth',
            'customer_address_id',
            'description',
            'group_name',
            'hand_off_point',
            'install_date',
            'decommission_date',
            'properties',
            'reference',
            'service_provider_address_id',
        )

    def validate_bandwidth(self, bandwidth: Optional[int]) -> Optional[str]:
        """
        description: The bandwidth of the Circuit
        required: false
        type: integer
        """
        if bandwidth is None:
            return None
        try:
            bandwidth = int(bandwidth)
        except (ValueError, TypeError):
            return 'circuit_circuit_update_101'
        self.cleaned_data['bandwidth'] = bandwidth
        return None

    def validate_customer_address_id(self, customer_address_id: Optional[int]) -> Optional[str]:
        """
        description: The Address ID of the customer for the Circuit
        type: integer
        """
        if not(customer_address_id):
            return None

        try:
            customer_address_id = int(customer_address_id)
        except (ValueError, TypeError):
            return 'circuit_circuit_update_103'

        if self.request.user.address['id'] != customer_address_id:
            response = Membership.address.read(
                token=self.request.user.token,
                pk=customer_address_id,
                span=self.span,
            )
            if response.status_code != 200:
                return 'circuit_circuit_update_104'
        self.cleaned_data['customer_address_id'] = customer_address_id
        return None

    def validate_description(self, description: Optional[str]) -> Optional[str]:
        """
        description: A description of the circuit.
        required: false
        type: string
        """
        self.cleaned_data['description'] = str(description).strip()
        return None

    def validate_group_name(self, group_name: Optional[str]) -> Optional[str]:
        """
        description: The group name of the circuit
        required: false
        type: string
        """
        if group_name is None:
            group_name = ''
        group_name = str(group_name).strip()
        if len(group_name) > self.get_field('group_name').max_length:
            return 'circuit_circuit_update_120'
        self.cleaned_data['group_name'] = group_name
        return None

    def validate_hand_off_point(self, hand_off_point: Optional[str]) -> Optional[str]:
        """
        description: The hand off point location for the circuit
        required: false
        type: string
        """
        if hand_off_point is None:
            hand_off_point = ''
        hand_off_point = str(hand_off_point).strip()
        if len(hand_off_point) > self.get_field('hand_off_point').max_length:
            return 'circuit_circuit_update_105'
        self.cleaned_data['hand_off_point'] = hand_off_point
        return None

    def validate_install_date(self, install_date) -> Optional[str]:
        """
        description: Date Circuit was installed_date
        type: string
        """
        if install_date is None:
            return 'circuit_circuit_update_106'

        try:
            install_date = parser.parse(install_date)
        except(ValueError, TypeError):
            return 'circuit_circuit_update_107'

        self.cleaned_data['install_date'] = install_date
        return None

    def validate_decommission_date(self, decommission_date) -> Optional[str]:
        """
        description: Date Circuit was decommissioned
        required: false
        type: string
        """
        if decommission_date is None:
            return None

        try:
            decommission_date = parser.parse(decommission_date)
        except(ValueError, TypeError):
            return 'circuit_circuit_update_108'

        if 'install_date' in self._errors:
            # install date was sent in request and failed validation.
            return None
        install_date = self.cleaned_data.get('install_date', self._instance.install_date)
        # Check that it's valid compared to the install_date
        if decommission_date < install_date:
            return 'circuit_circuit_update_109'

        self.cleaned_data['decommission_date'] = decommission_date
        return None

    def validate_properties(self, properties: Optional[Dict[str, Any]]) -> Optional[str]:
        """
        description: |
            Properties is a dictionary of the property types associated with the assigned circuit class.
            If the Circuit Class has a property with required as True, then it must be included in the request.
            e.g. Circuit Class has "height-cm" and "width-cm" as properties and required is True for "height"
                {
                    'height-cm': 25,
                }
            This will pass because the "width-cm" is not required.
        type: dict
        """
        if self._instance.circuit_class.properties.count() == 0:
            # Circuit Class has no properties
            return None
        if not isinstance(properties, dict):
            return 'circuit_circuit_update_110'
        for p in self._instance.circuit_class.properties.all():
            if p.key in properties:
                if p.required:
                    if properties.get(p.key) is None:
                        return 'circuit_circuit_update_111'
                value = properties.get(p.key)
                if value:
                    if p.property_type_id == 1:
                        value = str(value)
                    elif p.property_type_id == 2:
                        if not isinstance(value, (int, float, complex, Decimal)):
                            return 'circuit_circuit_update_112'
                    elif p.property_type_id == 3:
                        if not isinstance(value, bool):
                            return None
                    elif p.property_type_id == 4:
                        result = urlparse(value)
                        if not all([result.scheme, result.netloc]):
                            return 'circuit_circuit_update_113'
                    elif p.property_type_id == 5:
                        try:
                            IPNetwork(value)
                        except (TypeError, ValueError, AddrFormatError):
                            return 'circuit_circuit_update_114'
            else:
                if p.required:
                    return 'circuit_circuit_update_115'
                properties.update({p.key: None})

        self.cleaned_data['properties'] = properties
        return None

    def validate_reference(self, reference: Optional[str]) -> Optional[str]:
        """
        description: The reference for this Circuit
        required: false
        type: string
        """
        if reference is None:
            reference = ''
        reference = str(reference).strip()
        if len(reference) > self.get_field('reference').max_length:
            return 'circuit_circuit_update_116'
        self.cleaned_data['reference'] = reference
        return None

    def validate_service_provider_address_id(self, service_provider_address_id: Optional[int]) -> Optional[str]:
        """
        description: The Address ID of the service_provider for the Circuit
        type: integer
        """
        if not(service_provider_address_id):
            return None

        try:
            service_provider_address_id = int(service_provider_address_id)
        except (ValueError, TypeError):
            return 'circuit_circuit_update_118'

        if self.request.user.address['id'] != service_provider_address_id:
            response = Membership.address.read(
                token=self.request.user.token,
                pk=service_provider_address_id,
                span=self.span,
            )
            if response.status_code != 200:
                return 'circuit_circuit_update_119'
        self.cleaned_data['service_provider_address_id'] = service_provider_address_id
        return None
