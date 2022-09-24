
from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('<int:incident_id>/', views.incident, name='incident'),
  path('incidents/<int:incident_id>/updateincident/', views.update_incident, name="updateIncident"),
  path('createincident/', views.createIncident, name ="createIncident"),
  path('search', views.search, name='search'),
]