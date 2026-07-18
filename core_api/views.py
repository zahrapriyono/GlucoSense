from django.http import JsonResponse
from .models import Article, Doctor

def get_articles(request):
    # Mengambil semua data artikel dari database menggunakan snake_case
    articles = Article.objects.all().order_by('createdAt')
    
    data = []
    for article in articles:
        data.append({
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "category": article.category,
            "createdAt": article.createdAt.isoformat() if article.createdAt else None
        })
        
    return JsonResponse(data, safe=False)

def get_doctors(request):
    # Mengambil parameter filter dari URL menggunakan snake_case
    city_filter = request.GET.get('city', None)
    experience_filter = request.GET.get('experience', None)
    
    doctors = Doctor.objects.all()
    
    # Menerapkan filter
    if city_filter:
        doctors = doctors.filter(city__iexact=city_filter)
    if experience_filter:
        doctors = doctors.filter(experience_years__gte=int(experience_filter))
        
    data = []
    for doctor in doctors:
        data.append({
            "id": doctor.id,
            "full_name": doctor.fullName,
            "specialization": doctor.specialization,
            "city": doctor.city,
            "experience_years": doctor.experienceYears,
            "description": doctor.description,
            "createdAt": doctor.createdAt.isoformat() if doctor.createdAt else None
        })
        
    return JsonResponse(data, safe=False)