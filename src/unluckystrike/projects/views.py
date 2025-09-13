from django.shortcuts import render, get_object_or_404
from projects.models import Project, ETF, Dividend

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
    elif project == 'etf':
        return etf_view(request)
    else:
        return render(request, '#')
    

def lottery_view(request):
    now = datetime.now()
    lottery_number = []

    while(len(lottery_number) < 6):
        ran_num = random.randrange(1, 46)

        if (ran_num in lottery_number):
            continue

        lottery_number.append(ran_num)

    lottery_number.sort()

    context = {
        "now_date": now.strftime('%Y-%m-%d %H:%M:%S'),
        "lottery_number": lottery_number,
    }

    return render(request, 'lottery.html', context)


def exchange_rate_view(request):

    return render(request, 'exchange-rate.html')

def etf_view(request):
    etf_list = ETF.objects.all()
    return render(request, 'etf_base.html', {'etf_list': etf_list})

def etf_detail_view(request, etf_id):
    etf = get_object_or_404(ETF, id=etf_id)
    dividends = Dividend.objects.filter(etf=etf).order_by('paid_date')
    labels = [div.paid_date.strftime('%Y-%m-%d') for div in dividends]
    amounts = [float(div.amount) for div in dividends]
    currency = dividends[0].currency.code if dividends else 'USD'  # 기본 통화 설정

    return render(request, 'etf_detail.html', {
        'etf': etf,
        'labels': labels,
        'amounts': amounts,
        'currency': currency,
    })