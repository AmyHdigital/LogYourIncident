
from django.urls import path

import incidents

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('about', views.about, name='about'),

]