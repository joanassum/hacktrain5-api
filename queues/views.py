from django.shortcuts import render
from django.http import HttpResponse
import time, threading

# Create your views here.

opened_queue = 4
queue_population = [0] * opened_queue
large_luggages_weight = 2
small_luggages_weight = 1
no_of_ppl_weight = 1
no_of_kids_weight = 2

decrease_time_interval = 5

def decrease_population():
    print(time.ctime())
    queue_population[:] = [ max(0, x - 1) for x in queue_population ]
    print(queue_population)
    threading.Timer(decrease_time_interval, decrease_population).start()

decrease_population()

def allocate(request):
    queue_number = queue_population.index(min(queue_population))
    large_luggages = int(request.GET.get('large_luggages'))
    small_luggages = int(request.GET.get('small_luggages'))
    no_of_ppl = int(request.GET.get('no_of_ppl'))
    no_of_kids = int(request.GET.get('no_of_kids'))
    print(queue_population)
    queue_population[queue_number] += large_luggages_weight * large_luggages
    queue_population[queue_number] += small_luggages_weight * small_luggages
    queue_population[queue_number] += no_of_ppl_weight * no_of_ppl
    queue_population[queue_number] += no_of_kids_weight * no_of_kids
    print(queue_population)
    return HttpResponse(queue_number)

def queues(request):
    queues_json = {
        "queues": queue_population
    }
    return HttpResponse(queues_json)
