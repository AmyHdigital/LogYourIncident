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
def index(request):
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

    #myFilters = IncidentFilter (request.GET, queryset=Incident.objects.all())
    context = {
        'users': User.objects.all(),
        'priority_choices': Priority.choices,
        'status_choices': Status.choices,
        'systems': System.objects.all(),
        'incidents' : paged_incidents
        
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

    if request.GET.get('button') == 'resolve':
        this_incident.status = Status.RESOLVED
        this_incident.resolvedOn = timezone.now()
        messages.success(request,'Incident Resolved')
    elif request.GET.get('button') == 'unassign':
        this_incident.status = Status.RAISED
        this_incident.ownedBy = None
        messages.success(request,'Incident unassigned')
    elif request.GET.get('button') == 'assign':
        this_incident.status = Status.IN_PROGRESS
        this_incident.ownedBy = request.user
    elif request.GET.get('button') == 'close':
        this_incident.status = Status.CLOSED
        this_incident.closedOn = timezone.now()
        messages.success(request,'Incident Closed')
    elif request.GET.get('button') == 'delete':
        IncidentComment.objects.filter(incidentId=incident_id).delete()
        this_incident.delete()
        messages.success(request,'Incident Deleted')
    elif request.GET['addcomment'] and request.GET['comment']:
        createComment = IncidentComment.objects.create(
            incidentId = this_incident,
            userId = request.user,
            commentTime = timezone.now(),
            comment = request.GET['comment']).save()
        messages.success(request,'Comment saved')
    elif request.GET['addcomment'] and  not request.GET['comment']:
        messages.error(request,'Comment is empty and has not been saved')
        return redirect('/incidents/' + str(incident_id))

    this_incident.save()

    return redirect('/incidents/')


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
        'incidents' : paged_incidents
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