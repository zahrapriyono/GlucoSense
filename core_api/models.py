from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. MODUL UTAMA: ARTIKEL & DOKTER
# ==========================================

class Article(models.Model):
    title = models.CharField(max_length=255, db_column='title')
    content = models.TextField(db_column='content')
    category = models.CharField(max_length=50, db_column='category') # Contoh: 'Type 1', 'Type 2', 'Gestational'
    thumbnailUrl = models.URLField(max_length=500, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        db_table = 'articles'

    def __str__(self):
        return self.title

class SavedArticle(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='saved_articles',
        db_column='userId'
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='saved_by_users',
        db_column='articleId'
    )

    createdAt = models.DateTimeField(
        auto_now_add=True,
        db_column='createdAt'
    )

    class Meta:
        db_table = 'savedArticles'
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"


class Doctor(models.Model):
    fullName = models.CharField(max_length=255, db_column='fullName')
    specialization = models.CharField(max_length=100, db_column='specialization', default='Endocrinologist')
    city = models.CharField(max_length=100, db_column='city')
    experienceYears = models.IntegerField(db_column='experienceYears')
    description = models.TextField(db_column='description', blank=True, null=True)
    profilePictureUrl = models.URLField(max_length=500, blank=True, null=True)
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
# 3. MODUL ASSESSMENT
# ==========================================

class Assessment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assessments',
        db_column='userId'
    )

    # Assessment result
    probability = models.FloatField(db_column='probability')
    tier = models.CharField(max_length=20, db_column='tier')
    level = models.PositiveSmallIntegerField(db_column='level')

    # BRFSS features used by the ML model
    highBP = models.IntegerField(db_column='HighBP')
    highChol = models.IntegerField(db_column='HighChol')
    cholCheck = models.IntegerField(db_column='CholCheck')
    bmi = models.FloatField(db_column='BMI')
    smoker = models.IntegerField(db_column='Smoker')
    stroke = models.IntegerField(db_column='Stroke')
    heartDiseaseOrAttack = models.IntegerField(
        db_column='HeartDiseaseorAttack'
    )
    physActivity = models.IntegerField(db_column='PhysActivity')
    fruits = models.IntegerField(db_column='Fruits')
    veggies = models.IntegerField(db_column='Veggies')
    hvyAlcoholConsump = models.IntegerField(
        db_column='HvyAlcoholConsump'
    )
    anyHealthcare = models.IntegerField(db_column='AnyHealthcare')
    noDocbcCost = models.IntegerField(db_column='NoDocbcCost')
    genHlth = models.IntegerField(db_column='GenHlth')
    mentHlth = models.IntegerField(db_column='MentHlth')
    physHlth = models.IntegerField(db_column='PhysHlth')
    diffWalk = models.IntegerField(db_column='DiffWalk')
    sex = models.IntegerField(db_column='Sex')
    age = models.IntegerField(db_column='Age')
    education = models.IntegerField(db_column='Education')
    income = models.IntegerField(db_column='Income')

    createdAt = models.DateTimeField(
        auto_now_add=True,
        db_column='createdAt'
    )

    class Meta:
        db_table = 'assessments'
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.user.username} - {self.tier} Risk ({self.probability}%)"


# ==========================================
# 4. MODUL TRACKER & INTERAKTIF
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
# 5. MODUL CHATBOT (UNTUK RIWAYAT CHAT ZAZA)
# ==========================================

class ChatHistory(models.Model):
    medicalProfile = models.ForeignKey(MedicalProfile, on_delete=models.CASCADE, db_column='medicalProfileId')
    userMessage = models.TextField(db_column='userMessage')
    aiResponse = models.TextField(db_column='aiResponse')
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        db_table = 'chatHistories'