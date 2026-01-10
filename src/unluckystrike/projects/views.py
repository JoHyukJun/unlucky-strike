from django.shortcuts import render, get_object_or_404
from projects.models import Project, ETF, Dividend

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
    elif project == 'system-monitoring':
        return system_monitoring_view(request)
        return SystemMonitoringAPIView.as_view()(request)
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

def etf_detail_view(request, ticker):
    etf = get_object_or_404(ETF, ticker=ticker)
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

def get_cpu_info():
    try:
        result = subprocess.run(['nproc'], capture_output=True, text=True)
        cpu_count = int(result.stdout.strip())
        
        # 간단한 CPU 사용률 (top 명령어 사용, 부정확하지만 대안)
        result = subprocess.run(['top', '-bn1'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if 'Cpu(s)' in line:
                # 예: %Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
                parts = line.split()
                idle = float(parts[7].rstrip(','))
                cpu_percent = 100.0 - idle
                break
        else:
            cpu_percent = 0.0
        
        # CPU 주파수 (lscpu 사용)
        result = subprocess.run(['lscpu'], capture_output=True, text=True)
        cpu_freq = 0
        for line in result.stdout.split('\n'):
            if 'CPU MHz:' in line:
                cpu_freq = float(line.split(':')[1].strip())
                break
        
        return cpu_percent, cpu_count, cpu_freq
    except Exception as e:
        return 0.0, 1, 0

def get_memory_info():
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        mem_total = 0
        mem_available = 0
        for line in lines:
            if line.startswith('MemTotal:'):
                mem_total = int(line.split()[1]) * 1024  # KB to bytes
            elif line.startswith('MemAvailable:'):
                mem_available = int(line.split()[1]) * 1024
        mem_used = mem_total - mem_available
        memory_percent = (mem_used / mem_total) * 100 if mem_total > 0 else 0
        memory_used_gb = mem_used / (1024**3)
        memory_total_gb = mem_total / (1024**3)
        return memory_percent, memory_used_gb, memory_total_gb
    except Exception as e:
        return 0.0, 0.0, 1.0

def get_disk_info():
    try:
        result = subprocess.run(['df', '/'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            disk_total = int(parts[1]) * 1024  # KB to bytes
            disk_used = int(parts[2]) * 1024
            disk_percent = (disk_used / disk_total) * 100 if disk_total > 0 else 0
            disk_used_gb = disk_used / (1024**3)
            disk_total_gb = disk_total / (1024**3)
            return disk_percent, disk_used_gb, disk_total_gb
    except Exception as e:
        pass
    return 0.0, 0.0, 1.0

def get_network_info():
    try:
        with open('/proc/net/dev', 'r') as f:
            lines = f.readlines()
        for line in lines[2:]:  # 헤더 건너뛰기
            parts = line.split()
            if parts[0].strip(':') == 'eth0' or parts[0].strip(':') == 'wlan0':  # 인터페이스 선택
                net_recv = int(parts[1]) / (1024**2)  # bytes to MB
                net_sent = int(parts[9]) / (1024**2)
                return net_sent, net_recv
    except Exception as e:
        pass
    return 0.0, 0.0

def get_uptime():
    try:
        result = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return "Unknown"
    
def system_monitoring_view(request):
    cpu_percent, cpu_count, cpu_freq = get_cpu_info()
    memory_percent, memory_used, memory_total = get_memory_info()
    disk_percent, disk_used, disk_total = get_disk_info()
    net_sent, net_recv = get_network_info()
    uptime = get_uptime()

    context = {
        'cpu_percent': round(cpu_percent, 1),
        'cpu_count': cpu_count,
        'cpu_freq': round(cpu_freq, 0),
        'memory_percent': round(memory_percent, 1),
        'memory_used': round(memory_used, 2),
        'memory_total': round(memory_total, 2),
        'disk_percent': round(disk_percent, 1),
        'disk_used': round(disk_used, 2),
        'disk_total': round(disk_total, 2),
        'net_sent': round(net_sent, 2),
        'net_recv': round(net_recv, 2),
        'uptime': uptime,
    }

    return render(request, 'system-monitoring.html', context)

class SystemMonitoringAPIView(APIView):
    def get(self, request):
        # CPU 정보
        cpu_percent = get_cpu_info()[0]

        # 메모리 정보
        memory_percent, memory_used, _ = get_memory_info()

        # 디스크 정보
        disk_percent, disk_used, _ = get_disk_info()

        # 네트워크 정보
        net_sent, net_recv = get_network_info()

        data = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'memory_used': round(memory_used, 2),
            'disk_percent': disk_percent,
            'disk_used': round(disk_used, 2),
            'net_sent': round(net_sent, 2),
            'net_recv': round(net_recv, 2),
        }

        return Response(data, status=status.HTTP_200_OK)