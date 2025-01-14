# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse
# local
from .circuit_class import CircuitClass


__all__ = [
    'Circuit',
]


class CircuitManager(BaseManager):
    """
    Manager for Circuit which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().select_related(
            'circuit_class',
        )


class Circuit(BaseModel):
    """
    The Circuit model represents a circuit.
    """
    # Fields
    address_id = models.IntegerField()
    bandwidth = models.IntegerField(null=True)
    circuit_class = models.ForeignKey(CircuitClass, models.CASCADE, related_name='circuits')
    customer_address_id = models.IntegerField(null=True)
    decommission_date = models.DateTimeField(null=True)
    description = models.TextField()
    group_name = models.CharField(max_length=250, null=True)
    hand_off_point = models.CharField(max_length=20, null=True)
    install_date = models.DateTimeField()
    properties = models.JSONField(default=dict)
    reference_number = models.IntegerField()
    reference = models.CharField(max_length=100, null=True, default='')
    service_provider_address_id = models.IntegerField(null=True)

    objects = CircuitManager()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'circuit'
        indexes = [
            models.Index(fields=['id'], name='circuit_id'),
            models.Index(fields=['address_id'], name='circuit_address_id'),
            models.Index(fields=['customer_address_id'], name='circuit_customer_address_id'),
            models.Index(fields=['decommission_date'], name='circuit_decommission_date'),
            models.Index(fields=['group_name'], name='circuit_group_name'),
            models.Index(fields=['install_date'], name='circuit_install_date'),
            models.Index(fields=['reference_number'], name='circuit_reference_number'),
            models.Index(fields=['reference'], name='circuit_reference'),
            models.Index(fields=['service_provider_address_id'], name='circuit_sp_address_id'),
        ]

        ordering = ['reference_number']

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the CircuitResource view for this Circuit record
        :return: A URL that corresponds to the views for this Circuit record
        """
        return reverse('circuit_resource', kwargs={'pk': self.pk})
