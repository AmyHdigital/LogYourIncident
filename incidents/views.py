from pickle import NONE
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.views import login
from .models import Incident, IncidentComment, System, Status, Priority
from . import forms
import incidents
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from incidents.choices import raisedBy_choices, priority_choices, ownedBy_choices, status_choices
from django.utils import timezone


# Create your views here.

@login_required
def incidents(request):
    queryset_list = Incident.objects.all()

    if 'raisedBy' in request.GET:
        raisedBy = request.GET['raisedBy']
        if raisedBy:
            queryset_list = queryset_list.filter(reportedBy__exact=raisedBy)

    if 'ownedBy' in request.GET:
        ownedBy = request.GET['ownedBy']
        if ownedBy:
            queryset_list = queryset_list.filter(ownedBy__exact=ownedBy)

    if 'priority' in request.GET:
        priority = request.GET['priority']
        if priority:
            queryset_list = queryset_list.filter(priority__exact=priority)

    if 'status' in request.GET:
        status = request.GET['status']
        if status:
            queryset_list = queryset_list.filter(status__exact=status)

    if 'system' in request.GET:
        system = request.GET['system']
        if system:
            queryset_list = queryset_list.filter(system__exact=system)

    queryset_list = queryset_list.order_by('createdOn')
    paginator = Paginator(queryset_list, 5)
    page = request.GET.get('page')
    paged_incidents = paginator.get_page(page)

    # myFilters = IncidentFilter (request.GET, queryset=Incident.objects.all())
    context = {
        'users': User.objects.all(),
        'priority_choices': Priority.choices,
        'status_choices': Status.choices,
        'systems': System.objects.all(),
        'incidents': paged_incidents

    }

    return render(request, 'incidents/incidents.html', context)


def createIncident(request):
    if request.method == 'POST':
        description = request.POST['description']
        title = request.POST['title']
        systemId = request.POST['system']
        priority = request.POST['priority']
        # form = forms.IncidentForm()

        system = get_object_or_404(System, pk=systemId)

        createincident = Incident.objects.create(
            title=title, description=description, system=system, priority=priority, reportedBy=request.user)
        createincident.save()
        messages.success(request, 'Incident Saved')
        return redirect('/incidents/')
    else:
        form = forms.IncidentForm()
        return render(request, 'incidents/createIncident.html', {'form': form})


def update_incident(request, incident_id):
    this_incident = get_object_or_404(Incident, pk=incident_id)

    if request.method == 'POST' and 'resolve' in request.POST:
        this_incident.status = Status.RESOLVED
        this_incident.resolvedOn = timezone.now()
        messages.success(request, 'Incident Resolved')
        this_incident.save()
    elif request.method == 'POST' and 'unassign' in request.POST:
        unassignIncident(request,this_incident)
        # this_incident.status = Status.RAISED
        # this_incident.ownedBy = None
        # messages.success(request, 'Incident unassigned')
        # this_incident.save()
    elif request.method == 'POST' and 'assign' in request.POST:
        assignIncident(request, this_incident)
        # this_incident.status = Status.IN_PROGRESS
        # this_incident.ownedBy = request.user
        # this_incident.save()
    elif request.method == 'POST' and 'close' in request.POST:
        closeIncident(request,this_incident)
        # this_incident.status = Status.CLOSED
        # this_incident.closedOn = timezone.now()
        # messages.success(request, 'Incident Closed')
        # this_incident.save()
    elif request.method == 'POST' and 'delete' in request.POST:
        # IncidentComment.objects.filter(incidentId=incident_id).delete()
        # this_incident.delete()
        # messages.success(request,'Incident Deleted')
        deleteIncident(request, this_incident)
    elif request.method == 'POST' and request.POST['comment'] and 'addcomment' in request.POST:
        createComment = IncidentComment.objects.create(
            incidentId=this_incident,
            userId=request.user,
            commentTime=timezone.now(),
            comment=request.POST['comment']).save()
        messages.success(request, 'Comment saved')
        this_incident.save()
    elif request.method == 'POST' and not request.POST['comment'] and 'addcomment' in request.POST:
        messages.error(request, 'Comment is empty and has not been saved')
        return redirect('/incidents/' + str(incident_id))

    return redirect('/incidents/')


def deleteIncident(request, incident):
    if request.user.is_staff:
        IncidentComment.objects.filter(incidentId=incident.id).delete()
        incident.delete()
        messages.success(request, 'Incident Deleted')
    else:
        messages.warning(request, 'Only admin users can delete incidents.')


def assignIncident(request, incident):
    if incident.ownedBy == None:
        if request.user.id != incident.reportedBy.id:
            if incident.status == 'RA':
                incident.status = Status.IN_PROGRESS
                incident.ownedBy = request.user
                incident.save()
                messages.success(request, 'Incident assigned successfully')
            else:
                messages.warning(request, 'Incidents can only be assigned if the status is Raised')
        else:
            messages.warning(request, 'You cannot assign an incident raised by you')
    else:
        messages.warning(request, 'Incident already assigned')

def closeIncident(request, incident):
    if request.user.is_staff and incident.status == 'RE':
        incident.status = Status.CLOSED
        incident.closedOn = timezone.now()
        messages.success(request, 'Incident Closed')
        incident.save()
    else:
        messages.warning(request, 'Incident can only be closed by Admin')

def unassignIncident(request, incident):
    if request.user.is_staff:
        if incident.status == 'IP':
            if incident.ownedBy is not None:
                incident.status = Status.RAISED
                incident.ownedBy = None
                messages.success(request, 'Incident unassigned successfully')
                incident.save()
            else:
                messages.warning(request, 'This incident is already unassigned')
        else:
            messages.warning(request, 'This incident is not in-progress')
    else:
        messages.warning(request, 'Incident can only be unassigned by Admin')



def search(request):
    queryset_list = Incident.objects.all()

    if 'raisedBy' in request.GET:
        raisedBy = request.GET['raisedBy']
        if raisedBy:
            queryset_list = queryset_list.filter(reportedBy__exact=raisedBy)

    if 'ownedBy' in request.GET:
        ownedBy = request.GET['ownedBy']
        if ownedBy:
            queryset_list = queryset_list.filter(ownedBy__exact=ownedBy)

    if 'priority' in request.GET:
        priority = request.GET['priority']
        if priority:
            queryset_list = queryset_list.filter(priority__exact=priority)

    if 'status' in request.GET:
        status = request.GET['status']
        if status:
            queryset_list = queryset_list.filter(status__exact=status)

    if 'system' in request.GET:
        system = request.GET['system']
        if system:
            queryset_list = queryset_list.filter(system__exact=system)

    paginator = Paginator(queryset_list, 5)
    page = request.GET.get('page')
    paged_incidents = paginator.get_page(page)

    context = {

        'users': User.objects.all(),
        'priority_choices': Priority.choices,
        'status_choices': Status.choices,
        'systems': System.objects.all(),
        'incidents': paged_incidents
    }

    return render(request, 'incidents/incidents.html', context)


def about(request):
    return render(request, 'pages/about.html')


@login_required
def incident(request, incident_id):
    this_incident = get_object_or_404(Incident, pk=incident_id)
    incident_comments = IncidentComment.objects.filter(incidentId=incident_id)
    if request.method == "POST":
        if request.POST.get('assign'):
            this_incident.ownedBy = request.user
            this_incident.status = Status.IN_PROGRESS
        elif request.POST.get('unassign'):
            this_incident.ownedBy = None
            this_incident.status = Status.RAISED
        this_incident.save()

    return render(request, 'incidents/incident.html',
                  {'incident': this_incident, 'incident_comments': incident_comments})
