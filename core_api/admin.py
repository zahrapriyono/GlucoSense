from django.contrib import admin
from .models import Article, Doctor, MedicalProfile, BloodGlucoseLog, FoodLog, FavoriteDoctor, ChatHistory

# Mendaftarkan modul utama agar admin bisa mengisi konten
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'createdAt')
    list_filter = ('category',)
    search_fields = ('title', 'content')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('fullName', 'specialization', 'city', 'experienceYears')
    list_filter = ('city', 'specialization')
    search_fields = ('fullName', 'city')

# Mendaftarkan model lainnya agar terpantau di panel admin (opsional untuk monitoring)
admin.site.register(MedicalProfile)
admin.site.register(BloodGlucoseLog)
admin.site.register(FoodLog)
admin.site.register(FavoriteDoctor)
admin.site.register(ChatHistory)