from django.shortcuts import render
from projects.models import Project

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from datetime import datetime
import random
import requests, json

# Create your views here.
def project_index(request):
    return render(request, 'project_index.html')


def project_detail(request, project):
    if project == 'cognitive-services':
        return render(request, 'cognitive-services.html')
    elif project == 'image-processing':
        return render(request, 'image-processing.html')
    elif project == 'object-detection':
        return render(request, 'object-detection.html')
    elif project == 'raspberry-pi-lab':
        return render(request, 'raspberry-pi-lab.html')
    elif project == 'deep-learning-for-advanced-driver-assistance-system-applications':
        return render(request, 'deep-learning-for-advanced-driver-assistance-system-applications.html')
    elif project == 'open-webcam-test':
        return render(request, 'open-webcam-test.html')
    elif project == 'lottery':
        return lottery_view(request)
    elif project == 'exchange-rate':
        return exchange_rate_view(request)
    else:
        return render(request, '#')
    

def lottery_view(request):
    now = datetime.now()
    lottery_number = []

    for i in range(6):
        lottery_number.append(random.randrange(1, 46))

    lottery_number.sort()

    context = {
        "now_date": now.strftime('%Y-%m-%d %H:%M:%S'),
        "lottery_number": lottery_number,
    }

    return render(request, 'lottery.html', context)


def exchange_rate_view(request):

    return render(request, 'exchange-rate.html')