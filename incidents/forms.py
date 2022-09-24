from django.forms import ModelForm, Select, TextInput
from .models import Incident


class IncidentForm(ModelForm): 
    class Meta:
        model = Incident
        fields = ('title', 'description', 'system', 'priority')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'system': Select(attrs={'class': 'form-control'}),
            'priority': Select(attrs={'class': 'form-control'})
        }
