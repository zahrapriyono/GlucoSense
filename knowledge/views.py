from django.shortcuts import render
from core_api.models import Article

def list_articles(request):
    articles = Article.objects.all().order_by('createdAt')

    return render(
        request,
        'knowledge/list.html',
        {'articles': articles}
    )

def detail(request, article_id):
    return render(
        request,
        'knowledge/detail.html',
        {'article_id': article_id}
    )