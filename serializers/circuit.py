# libs
import serpy
# local
from .circuit_class import CircuitClassSerializer


__all__ = [
    'CircuitSerializer',
]


class CircuitSerializer(serpy.Serializer):
    """
    address_id:
        description: ID of address of circuit record
        type: integer
    bandwidth:
        description: bandwidth of circuit record
        type: integer
    circuit_class:
        $ref: '#/components/schemas/CircuitClass'
    circuit_class_id:
        description: circuit_class_id of circuit record
        type: integer
    created:
        description: Timestamp, in ISO format, of when the Circuit record was created.
        type: integer
    customer_address_id:
        description: customer_address_id of circuit record
        type: integer
    decommission_date:
        description: Timestamp, in ISO format, of when the Circuit was decommissioned.
        type: string
    description:
        description: Description of Circuit.
        type: string
    group_name:
        description: Group name of Circuit.
        type: string
    hand_off_point:
        description: The hand off point location for the Circuit.
        type: string
    id:
        description: ID of Circuit record
        type: integer
    install_date:
        description: Timestamp, in ISO format, of when the Circuit Class record was installed.
        type: string
    properties:
        description: The Properties assigned to the Circuit Class.
        type: array
        items:
            type: object
            properties:
                key:
                    description: The key(s) is user defined based on the properties assigned to the circuit class
                    type: string
    reference:
        description: A reference for the Circuit.
        type: string
    reference_number:
        description: The reference number of Circuit record
        type: integer
    service_provider_address_id:
        description: The service_provider_address_id of Circuit record
        type: integer
    updated:
        description: Timestamp, in ISO format, of when the Circuit record was updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the Circuit instance.
        type: string
        format: url
    """
    address_id = serpy.Field()
    bandwidth = serpy.Field()
    circuit_class = CircuitClassSerializer()
    circuit_class_id = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    customer_address_id = serpy.Field()
    decommission_date = serpy.Field(attr='decommission_date.isoformat', call=True, required=False)
    description = serpy.Field()
    group_name = serpy.Field()
    hand_off_point = serpy.Field()
    id = serpy.Field()
    install_date = serpy.Field(attr='install_date.isoformat', call=True)
    properties = serpy.Field()
    reference = serpy.Field()
    reference_number = serpy.Field()
    service_provider_address_id = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
