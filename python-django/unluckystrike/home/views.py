from django.shortcuts import render

# Create your views here.
def home_index(request):
    return render(request, 'home_index.html')


def work_detail(request, work):
    if work == 'cognitive-services':
        return render(request, 'cognitive-services.html')
    elif work == 'image-processing':
        return render(request, 'image-processing.html')
    elif work == 'object-detection':
        return render(request, 'object-detection.html')
    elif work == 'raspberry-pi-lab':
        return render(request, 'raspberry-pi-lab.html')
    elif work == 'deep-learning-for-advanced-driver-assistance-system-applications':
        return render(request, 'deep-learning-for-advanced-driver-assistance-system-applications.html')
    else:
        return render(request, '#')

