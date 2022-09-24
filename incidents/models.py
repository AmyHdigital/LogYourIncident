from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import django_filters


class System(models.Model):

  name = models.CharField(max_length=20, null=False, blank=False)
  description = models.CharField(max_length=100, null=True, blank=True)

  def __str__(self):
      return self.name


class Status(models.TextChoices):
    RAISED = 'RA', _('Raised')
    IN_PROGRESS = 'IP', _('In Progress')
    RESOLVED = 'RE', _('Resolved')
    CLOSED = 'CL', _('Closed')


class Priority(models.TextChoices):
    HIGH = 'H', _('High')
    MEDIUM = 'M', _('Medium')
    LOW = 'L', _('Low')
    

class Incident(models.Model):

    title = models.CharField(max_length=50, blank=False, default="")
    description = models.CharField(max_length=200, default="")
    createdOn = models.DateTimeField(default=timezone.now, null=False, blank=False)
    resolvedOn = models.DateTimeField(null=True, blank=True)
    closedOn = models.DateTimeField(null=True, blank=True)
    reportedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
    priority = models.CharField(max_length=1, choices=Priority.choices, default=Priority.LOW)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.RAISED)
    ownedBy = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='owner')
    system = models.ForeignKey(System, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class IncidentComment(models.Model):
  incidentId = models.ForeignKey(Incident, on_delete=models.CASCADE)
  userId = models.ForeignKey(User, on_delete=models.CASCADE)
  commentTime = models.DateTimeField(default=timezone.now)
  comment = models.CharField(max_length=1000, null=False, blank=False)

  def __str__(self):
        return self.comment



