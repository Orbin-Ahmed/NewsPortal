from django.shortcuts import render


# Create your views here.


def login(request):
    return render(request, 'auth/login.html')


def reporter_dashboard(request):
    return render(request, 'reporter/newReport.html')
