from django.shortcuts import render

def list_doctors(request):
    return render(request, 'doctors/list.html')