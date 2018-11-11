from django.urls import path

from . import views

urlpatterns = [

    path('allocate/', views.allocate, name='allocate'),
    path('queues/', views.queues, name='queues'),
    path('staff_number', views.staff_number, name='staff_number'),
]
