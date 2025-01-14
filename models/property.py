# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
# local
from .circuit_class import CircuitClass
from .property_type import PropertyType


__all__ = [
    'Property',
]


class PropertyManager(BaseManager):
    """
    Manager for Circuit Class which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().select_related(
            'property_type',
        )


class Property(BaseModel):
    """
    The Property model represents a property related to a circuit class.
    """
    # Fields
    circuit_class = models.ForeignKey(CircuitClass, models.PROTECT, related_name='properties')
    property_type = models.ForeignKey(PropertyType, models.PROTECT)
    key = models.CharField(max_length=250)
    required = models.BooleanField()

    objects = PropertyManager()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'property'
        indexes = [
            models.Index(fields=['id'], name='property_id'),
            models.Index(fields=['key'], name='property_key'),
            models.Index(fields=['required'], name='property_required'),
        ]

        ordering = ['key']
