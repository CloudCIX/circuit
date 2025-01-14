# libs
import serpy
# local
from .property_type import PropertyTypeSerializer


__all__ = [
    'PropertySerializer',
]


class PropertySerializer(serpy.Serializer):
    """
    key:
        description: The key name for the property
        type: string
    property_type:
        $ref: '#/components/schemas/PropertyType'
    property_type_id:
        description: ID of Property Type record assigned to the Property instance.
        type: integer
    required:
        description: A flag stating if the Property Key is required when creating a Circuit.
        type: boolean
    """
    key = serpy.Field()
    property_type = PropertyTypeSerializer()
    property_type_id = serpy.Field()
    required = serpy.Field()
