from django.shortcuts import render

def list_articles(request):
    return render(request, 'knowledge/list.html')

def detail(request, slug):
    return render(request, 'knowledge/detail.html')
