from django.shortcuts import render

def list_articles(request):
    articles = [
        {
            'title': 'The Glycemic Index: A Complete Guide',
            'category': 'NUTRITION',
            'excerpt': 'Understand how different foods impact your blood sugar...',
            'read_time': '5 min read',
            'slug': 'glycemic-index-guide',
            'image': '<https://picsum.photos/400/250?random=1>',
        },
        {
            'title': 'Intermittent Fasting and Glucose Control',
            'category': 'LIFESTYLE',
            'excerpt': 'New research suggests timing might be just as important...',
            'read_time': '8 min read',
            'slug': 'intermittent-fasting-glucose',
            'image': '<https://picsum.photos/400/250?random=2>',
        },
        {
            'title': 'Genetic Markers: Identifying Risk Before Symptoms',
            'category': 'RESEARCH',
            'excerpt': 'How personalized medicine is changing the way we screen...',
            'read_time': '12 min read',
            'slug': 'genetic-markers-risk',
            'image': '<https://picsum.photos/400/250?random=3>',
        },
        {
            'title': 'Superfoods for Glucose Balance',
            'category': 'HEALTHY LIVING',
            'excerpt': 'Discover the power of phytonutrients that help stabilize blood sugar...',
            'read_time': '6 min read',
            'slug': 'superfoods-glucose',
            'image': '<https://picsum.photos/400/250?random=4>',
        },
    ]
    return render(request, 'knowledge/list.html', {'articles': articles})

def detail(request, slug):
    return render(request, 'knowledge/detail.html')
