from django.shortcuts import render

def list_articles(request):
    articles = [
        {
            'image': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600&h=300&fit=crop',
            'category': 'NUTRITION',
            'title': 'The Glycemic Index: A Complete Guide',
            'excerpt': 'Understand how different foods impact your blood sugar and make smarter choices daily.',
            'read_time': '5 min read',
            'slug': 'glycemic-index-guide',
        },
        {
            'image': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&h=300&fit=crop',
            'category': 'LIFESTYLE',
            'title': 'Intermittent Fasting and Glucose Control',
            'excerpt': 'New research suggests timing your meals is just as important as what you eat.',
            'read_time': '8 min read',
            'slug': 'intermittent-fasting',
        },
        {
            'image': 'https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=600&h=300&fit=crop',
            'category': 'RESEARCH',
            'title': 'Genetic Markers: Identifying Risk Before Symptoms',
            'excerpt': 'How personalized medicine is changing the way we screen for Type 2 diabetes.',
            'read_time': '12 min read',
            'slug': 'genetic-markers',
        },
        {
            'image': 'https://images.unsplash.com/photo-1505576399279-565b52d4ac71?w=600&h=300&fit=crop',
            'category': 'PREVENTION',
            'title': 'Exercise and Insulin Sensitivity',
            'excerpt': 'Even 30 minutes of walking can dramatically improve how your body processes glucose.',
            'read_time': '6 min read',
            'slug': 'exercise-insulin',
        },
        {
            'image': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&h=300&fit=crop',
            'category': 'HEALTHY LIVING',
            'title': 'Stress, Cortisol, and Blood Sugar Spikes',
            'excerpt': 'The connection between mental health and metabolic health is stronger than you think.',
            'read_time': '7 min read',
            'slug': 'stress-cortisol',
        },
        {
            'image': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=600&h=300&fit=crop',
            'category': 'TYPE 2',
            'title': 'Early Warning Signs You Shouldn\'t Ignore',
            'excerpt': 'Many people live with prediabetes for years without knowing. Here\'s what to watch for.',
            'read_time': '4 min read',
            'slug': 'early-warning-signs',
        },
    ]
    return render(request, 'knowledge/list.html', {'articles': articles})

def detail(request, slug):
    return render(request, 'knowledge/detail.html')
