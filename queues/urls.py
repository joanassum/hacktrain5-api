from django.urls import path

from . import views

urlpatterns = [

    path('allocate/', views.allocate, name='allocate'),
    path('queues/', views.queues, name='queues'),
]
