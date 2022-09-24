from django.contrib import admin

# Register your models here.
from .models import Incident, IncidentComment, System

admin.site.register(Incident)
admin.site.register(IncidentComment)
admin.site.register(System)