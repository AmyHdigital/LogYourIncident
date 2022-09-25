import django_filters

from .models import Incident, System



class IncidentFilter(django_filters.FilterSet):
  class Meta:
    model = Incident
    field = '__all__'
    exclude =  ['status', 'priority']
  