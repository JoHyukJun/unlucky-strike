from django.shortcuts import render

# Create your views here.


def service_index(request):
    return render(request, 'service_index.html')


def service_detail(request, service):
    if service == 'open_webcam_test':
        return render(request, 'open_webcam_test.html')
    elif service == 'random-access-music':
        return render(request, 'random-access-music.html')
    else:
        return render(request, '#')


def random_access_music(request):

    
    return