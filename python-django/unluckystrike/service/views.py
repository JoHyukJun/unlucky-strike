from django.shortcuts import render

# Create your views here.


def service_index(request):
    return render(request, 'service_index.html')


def service_detail(request, service):
    if service == 'open_webcam_test':
        return render(request, 'open_webcam_test.html')
    else:
        return render(request, '#')