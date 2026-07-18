from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. MODUL UTAMA: ARTIKEL & DOKTER
# ==========================================

class Article(models.Model):
    title = models.CharField(max_length=255, db_column='title')
    content = models.TextField(db_column='content')
    category = models.CharField(max_length=50, db_column='category') # Contoh: 'Type 1', 'Type 2', 'Gestational'
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        db_table = 'articles'

    def __str__(self):
        return self.title


class Doctor(models.Model):
    fullName = models.CharField(max_length=255, db_column='fullName')
    specialization = models.CharField(max_length=100, db_column='specialization', default='Endocrinologist')
    city = models.CharField(max_length=100, db_column='city')
    experienceYears = models.IntegerField(db_column='experienceYears')
    description = models.TextField(db_column='description', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        db_table = 'doctors'

    def __str__(self):
        return self.fullName


# ==========================================
# 2. MODUL USER: PROFIL MEDIS
# ==========================================

class MedicalProfile(models.Model):
    # Menghubungkan ke tabel user bawaan Django/Supabase Auth
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='userId')
    fullName = models.CharField(max_length=255, db_column='fullName')
    diabetesType = models.CharField(max_length=50, db_column='diabetesType') # 'Type 1', 'Type 2', dll
    targetSugarLow = models.IntegerField(db_column='targetSugarLow', default=70) # mg/dL
    targetSugarHigh = models.IntegerField(db_column='targetSugarHigh', default=140) # mg/dL
    birthDate = models.DateField(db_column='birthDate', blank=True, null=True)
    weightKg = models.DecimalField(max_digits=5, decimal_places=2, db_column='weightKg', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        db_table = 'medicalProfiles'

    def __str__(self):
        return f"Profile: {self.fullName}"


# ==========================================
# 3. MODUL TRACKER & INTERAKTIF
# ==========================================

class BloodGlucoseLog(models.Model):
    medicalProfile = models.ForeignKey(MedicalProfile, on_delete=models.CASCADE, db_column='medicalProfileId')
    sugarLevel = models.IntegerField(db_column='sugarLevel') # mg/dL
    logContext = models.CharField(max_length=100, db_column='logContext') # Contoh: 'Before Breakfast', 'After Lunch'
    loggedAt = models.DateTimeField(db_column='loggedAt')

    class Meta:
        db_table = 'bloodGlucoseLogs'


class FoodLog(models.Model):
    medicalProfile = models.ForeignKey(MedicalProfile, on_delete=models.CASCADE, db_column='medicalProfileId')
    foodName = models.CharField(max_length=255, db_column='foodName')
    estimatedCarbs = models.IntegerField(db_column='estimatedCarbs') # dalam gram
    loggedAt = models.DateTimeField(db_column='loggedAt')

    class Meta:
        db_table = 'foodLogs'


class FavoriteDoctor(models.Model):
    medicalProfile = models.ForeignKey(MedicalProfile, on_delete=models.CASCADE, db_column='medicalProfileId')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctorId')
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        db_table = 'favoriteDoctors'
        # Memastikan user tidak menduplikasi dokter favorit yang sama
        unique_together = ('medicalProfile', 'doctor') 


# ==========================================
# 4. MODUL CHATBOT (UNTUK RIWAYAT CHAT ZAZA)
# ==========================================

class ChatHistory(models.Model):
    medicalProfile = models.ForeignKey(MedicalProfile, on_delete=models.CASCADE, db_column='medicalProfileId')
    userMessage = models.TextField(db_column='userMessage')
    aiResponse = models.TextField(db_column='aiResponse')
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        db_table = 'chatHistories'