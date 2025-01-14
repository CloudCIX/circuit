# stdlib
from datetime import datetime
# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse
# local


__all__ = [
    'CircuitClass',
]


class CircuitClassManager(BaseManager):
    """
    Manager for Circuit Class which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().prefetch_related(
            'properties',
        )


class CircuitClass(BaseModel):
    """
    The CircuitClass model represents a class group for a circuit.
    """
    # Fields
    name = models.CharField(max_length=250)
    member_id = models.IntegerField()

    objects = CircuitClassManager()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'circuit_class'
        indexes = [
            models.Index(fields=['id'], name='circuit_class_id'),
            models.Index(fields=['name'], name='circuit_class_name'),
            models.Index(fields=['member_id'], name='circuit_class_member_id'),
        ]

        ordering = ['name']

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the CircuitClassResource view for this CircuitClass record
        :return: A URL that corresponds to the views for this CircuitClass record
        """
        return reverse('circuit_class_resource', kwargs={'pk': self.pk})

    def cascade_delete(self):
        """
        Delete the Circuit Class, and delete the Property records that are related to it
        """
        deltime = datetime.utcnow()
        for property in self.properties.all():
            property.deleted = deltime
            property.save()
        self.deleted = deltime
        self.save()

    @property
    def total_circuits(self):
        return self.circuits.filter(deleted__isnull=True).count()

    @property
    def total_properties(self):
        return self.properties.filter(deleted__isnull=True).count()
