from django.shortcuts import render
from django.http import HttpResponse
from statistics import mean
import time, threading
from websocket import create_connection

# Create your views here.

opened_queue = 4
queue_population = [0] * opened_queue
large_luggages_weight = 2
small_luggages_weight = 1
no_of_ppl_weight = 1
no_of_kids_weight = 4

no_of_staff_per_lane = 3

decrease_time_interval = 1
open_threshold = 80
ip = "172.20.10.6"

def get_queues():
    return queue_population

def decrease_population():
    print(time.ctime())
    queue_population[:] = [ max(0, x - 1) for x in queue_population ]
    print(queue_population)
    avg = sum(queue_population) / float(len(queue_population))
    level = ""
    if avg < 40:
        level = "Low"
    elif avg < 60:
        level = "Medium"
    else:
        level = "High"
    queues_json = {
        "queues": queue_population,
        "staff_number": max(4 * no_of_staff_per_lane, sum(queue_population) // 60 * no_of_staff_per_lane),
        "level": level
    }
    try:
        ws = create_connection("ws://" + ip + ":8000/ws/queues/")
        ws.send(str(queues_json))
        ws.close()
    except:
        print("Error")
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
    level = ""
    avg = sum(queue_population) / float(len(queue_population))
    if avg < 40:
        level = "Low"
    elif avg < 60:
        level = "Medium"
    else:
        level = "High"
    queues_json = {
        "queues": queue_population,
        "staff_number": staff_number(),
        "level": level
    }
    ws = create_connection("ws://" + ip + ":8000/ws/queues/")
    ws.send(str(queues_json))
    ws.close()
    # if mean(queue_population) > open_threshold and len(queue_population) < 8:
    #     queue_number = openNewGate()
    return HttpResponse(queue_number)

def queues(request):
    queues_json = {
        "queues": queue_population,
        "staff_number": staff_number()
    }
    return HttpResponse(queues_json)

def staff_number():
    staff_number = max(4 * no_of_staff_per_lane, sum(queue_population) // 60 * no_of_staff_per_lane)
    return staff_number

# def openNewGate():
#     queue_population.append(0)
#     return len(queue_population)
