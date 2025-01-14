from django.urls import include, path

urlpatterns = [
    path('', include('circuit.urls')),
]
