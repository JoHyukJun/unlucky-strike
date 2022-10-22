from django.shortcuts import render
from projects.models import Project


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
    else:
        return render(request, '#')