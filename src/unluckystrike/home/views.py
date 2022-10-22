from django.shortcuts import render

# Create your views here.
def home_index(request):
    return render(request, 'home_index.html')


def home_about(request):
    return render(request, 'about.html')


def home_contact(request):
    return render(request, 'contact.html')