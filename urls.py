from django.urls import path
from . import views

urlpatterns = [
    # Circuit
    path(
        'circuit/',
        views.CircuitCollection.as_view(),
        name='circuit_collection',
    ),

    path(
        'circuit/<int:pk>/',
        views.CircuitResource.as_view(),
        name='circuit_resource',
    ),
    # Circuit Class
    path(
        'circuit_class/',
        views.CircuitClassCollection.as_view(),
        name='circuit_class_collection',
    ),

    path(
        'circuit_class/<int:pk>/',
        views.CircuitClassResource.as_view(),
        name='circuit_class_resource',
    ),

    # Property Type
    path(
        'property_type/',
        views.PropertyTypeCollection.as_view(),
        name='property_type_collection',
    ),

    # property_value
    path(
        'property_value/<str:search_term>/',
        views.PropertyValueCollection.as_view(),
        name='property_value_collection',
    ),

]
