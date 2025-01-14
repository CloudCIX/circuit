# libs
import serpy
# local
from .property import PropertySerializer


__all__ = [
    'CircuitClassSerializer',
]


class CircuitClassSerializer(serpy.Serializer):
    """
    created:
        description: Timestamp, in ISO format, of when the Circuit Class record was created.
        type: integer
    id:
        description: ID of Circuit Class record
        type: integer
    name:
        description: Name of the Circuit Class record
        type: string
    member_id:
        description: The id of the Member that owns the Circuit Class record
        type: integer
    properties:
        description: The Properties assigned to the Circuit Class.
        type: array
        items:
            $ref: '#/components/schemas/Property'
    total_circuits:
        description: The number of Circuits that are associated with this Circuit Class.
        type: integer
    total_properties:
        description: The number of Properties this Circuit Class has.
        type: integer
    updated:
        description: Timestamp, in ISO format, of when the Circuit Class record was updated.
        type: integer
    uri:
        description: URL that can be used to run methods in the API associated with the Circuit Class instance.
        type: string
        format: url
    """
    created = serpy.Field(attr='created.isoformat', call=True)
    id = serpy.Field()
    name = serpy.Field()
    member_id = serpy.Field()
    properties = PropertySerializer(attr='properties.iterator', call=True, many=True)
    total_circuits = serpy.Field()
    total_properties = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
