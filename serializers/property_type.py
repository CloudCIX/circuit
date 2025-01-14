# libs
import serpy


__all__ = [
    'PropertyTypeSerializer',
]


class PropertyTypeSerializer(serpy.Serializer):
    """
    id:
        description: ID of Property Type record
        type: integer
    name:
        description: Name of the Property Type record
        type: string
    """
    id = serpy.Field()
    name = serpy.Field()
