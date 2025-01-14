# libs
from cloudcix_rest.controllers import ControllerBase


__all__ = [
    'PropertyTypeListController',
]


class PropertyTypeListController(ControllerBase):
    """
    Validates User data used to filter a list of PropertyType records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some ControllerBase.Meta fields to make them more
        specific for this Controller
        """

        allowed_ordering = (
            'id',
            'name',
        )
        search_fields = {
            'created': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'updated': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }
