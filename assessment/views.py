from django.shortcuts import render

def form(request):
    return render(request, 'assessment/form.html')

def result(request):
    return render(request, 'assessment/result.html')