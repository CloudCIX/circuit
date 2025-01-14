# libs
from cloudcix_rest.models import BaseModel
from django.db import models
# local


__all__ = [
    'PropertyType',
]


class PropertyType(BaseModel):
    """
    The PropertyType model represents a types that a property can be assigned.
    """
    # Fields
    name = models.CharField(max_length=250)

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'property_type'
        indexes = [
            models.Index(fields=['id'], name='property_type_id'),
            models.Index(fields=['name'], name='property_type_name'),
        ]

        ordering = ['name']
