from distutils.command.config import config
from django import views
from django.db import connection
from django.shortcuts import render

import pandas as pd

from .connect import mobvis_connection

def starting_page(request):
    context = {}

    if request.method == 'POST':
        trace = pd.read_csv(request.FILES['trace'], sep=',', header=None)
        
        print('\nUploaded trace: \n')
        print(trace.head())

        # 0: max_distance
        # 1: pause_threshold
        # 2: contact_radius
        # 3: distance_formula
        configurations = request.POST.getlist('configuration')

        metrics = request.POST.getlist('metric')

        plots = request.POST.getlist('plot')

        context = mobvis_connection(trace, configurations, metrics, plots)

    return render(request, 'home.html', context)