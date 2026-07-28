from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import (
    parse_json_body,
    success_response,
    error_response,
)

from .models import (
    Article,
    Doctor,
    MedicalProfile,
    BloodGlucoseLog,
    FoodLog,
)

# ==============================
# ARTICLE API
# ==============================

def get_article_list(request):

    """
    Mengambil semua daftar artikel edukasi diabetes.
    """
    articles = Article.objects.all().order_by('createdAt')
    data = []
    
    for article in articles:
        data.append({
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'thumbnailUrl': article.thumbnailUrl,
            'createdAt': article.createdAt.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    return JsonResponse(data, safe=False)


# ========================
# DOCTOR API
# ========================

def get_doctor_list(request):
    city_filter = request.GET.get('city', None)
    experience_filter = request.GET.get('experience', None)
    
    doctors = Doctor.objects.all()
    
    # Terapkan filter kota (case-insensitive / mengabaikan huruf besar-kecil)
    if city_filter:
        doctors = doctors.filter(city__iexact=city_filter)
        
    # Terapkan filter minimal pengalaman kerja
    if experience_filter:
        try:
            doctors = doctors.filter(experienceYears__gte=int(experience_filter))
        except ValueError:
            pass  # Mengabaikan filter jika input bukan angka valid
            
    data = []
    for doctor in doctors:
        data.append({
            'id': doctor.id,
            'fullName': doctor.fullName,
            'specialization': doctor.specialization,
            'city': doctor.city,
            'experienceYears': doctor.experienceYears,
            'profilePictureUrl': doctor.profilePictureUrl,
            'createdAt': doctor.createdAt.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    return JsonResponse(data, safe=False)


# =========================
# BLOOD GLUCOSE API
# =========================

def get_glucose_logs(request):
    profile_id = request.GET.get('profile_id', None)
    logs = BloodGlucoseLog.objects.all()

    if profile_id:
        logs = logs.filter(medicalProfile_id = profile_id)
        
    logs = logs.order_by('loggedAt')
    data = [
        {
            'id': log.id,
            'medical_profile_id': log.medicalProfile_id,
            'sugar_level': log.sugarLevel,
            'log_context': log.logContext,
            'logged_at': log.loggedAt.strftime('%Y-%m-%d %H:%M:%S'),
        }

        for log in logs
    ]

    return JsonResponse(data, safe=False)

def create_glucose_logs(request):
    body, error = parse_json_body(request)

    if error:
        return error

    medical_profile_id = body.get("medical_profile_id")
    sugar_level = body.get("sugar_level")
    log_context = body.get("log_context")
    logged_at = body.get("logged_at")

    if not all([
        medical_profile_id,
        sugar_level,
        log_context,
        logged_at,
    ]):
        return error_response(
            "All fields are required.",
            400
        )

    try:
        medical_profile = MedicalProfile.objects.get(id=medical_profile_id)
    except MedicalProfile.DoesNotExist:
        return error_response(
            "Medical profile not found.",
            404
        )

    glucose_log = BloodGlucoseLog.objects.create(
        medicalProfile=medical_profile,
        sugarLevel=sugar_level,
        logContext=log_context,
        loggedAt=logged_at,
    )
    return success_response(
        "Blood glucose log created successfully",
        status=201,
        id=glucose_log.id
    )

def update_glucose_logs(request):
    body, error = parse_json_body(request)

    if error:
        return error

    log_id = body.get("id")
    sugar_level = body.get("sugar_level")
    log_context = body.get("log_context")
    logged_at = body.get("logged_at")

    if not all([
        log_id,
        sugar_level,
        log_context,
        logged_at,
    ]):
        return error_response(
            "All fields are required.",
            400
        )

    try:
        glucose_log = BloodGlucoseLog.objects.get(id=log_id)
    except BloodGlucoseLog.DoesNotExist:
        return error_response(
            "Blood glucose log not found.",
            404
        )

    glucose_log.sugarLevel = sugar_level
    glucose_log.logContext = log_context
    glucose_log.loggedAt = logged_at

    glucose_log.save()

    return success_response(
        "Blood glucose log updeted successfully.",
        200
    )

def delete_glucose_log(request):
    body, error = parse_json_body(request)

    if error:
        return error

    log_id = body.get("id")

    if not log_id:
        return error_response(
            "Blood glucose log id is required.",
            400
        )

    try:
        glucose_log = BloodGlucoseLog.objects.get(id=log_id)
    except BloodGlucoseLog.DoesNotExist:
        return error_response(
            "Blood glucose log not found.",
            404
        )

    glucose_log.delete()

    return success_response(
        "Blood glucose log deleted successfully.",
        200
    )

@csrf_exempt
def glucose_log_api(request):

    if request.method == 'GET':
        return get_glucose_logs(request)
    
    elif request.method == "POST":
        return create_glucose_logs(request)
    
    elif request.method == "PUT":
        return update_glucose_logs(request)
    
    elif request.method == "DELETE":
        return delete_glucose_log(request)
    
    return error_response(
        "Method not allowed.",
        405
    )

# ===========================
# FOOD LOG API
# ===========================

def get_food_logs(request):
    profile_id = request.GET.get("profile_id", None)

    logs = FoodLog.objects.all()

    if profile_id:
        logs = logs.filter(
            medicalProfile_id = profile_id
        )

    logs = logs.order_by("loggedAt")

    data = [
        {
            "id": log.id,
            "medical_profile_id": log.medicalProfile_id,
            "food_name": log.foodName,
            "estimated_carbs": log.estimatedCarbs,
            "logged_at": log.loggedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }

        for log in logs
    ]

    return JsonResponse(data, safe=False)


def create_food_log(request):
    body ,error = parse_json_body(request)

    if error:
        return error

    medical_profile_id = body.get("medical_profile_id")
    food_name = body.get("food_name")
    estimated_carbs = body.get("estimated_carbs")
    logged_at = body.get("logged_at")

    if not all([
        medical_profile_id,
        food_name,
        estimated_carbs,
        logged_at
    ]):
        return error_response(
            "All fields are required.",
            400
        )

    try:
        medical_profile = MedicalProfile.objects.get(id=medical_profile_id)
    except MedicalProfile.DoesNotExist:
        return error_response(
            "Medical profile not found.",
            404
        )

    food_log = FoodLog.objects.create(
        medicalProfile=medical_profile,
        foodName=food_name,
        estimatedCarbs=estimated_carbs,
        loggedAt=logged_at,
    )

    return success_response(
        "Food log created successfully.",
        status=201,
        id=food_log.id,
    )

def update_food_log(request):
    body, error = parse_json_body(request)

    if error:
        return error

    log_id = body.get("id")
    food_name = body.get("food_name")
    estimated_carbs = body.get("estimated_carbs")
    logged_at = body.get("logged_at")

    if not all([
        log_id,
        food_name,
        estimated_carbs,
        logged_at,
    ]):
        return error_response(
            "All fields are required.",
            400
        )

    try:
        food_log = FoodLog.objects.get(id=log_id)
    except FoodLog.DoesNotExist:
        return error_response(
            "Food log not found.",
            404
        )

    food_log.foodName = food_name
    food_log.estimatedCarbs = estimated_carbs
    food_log.loggedAt = logged_at

    food_log.save()

    return success_response(
        "Food log updated successfully."
    )
    
def delete_food_log(request):
    body, error = parse_json_body(request)

    if error:
        return error

    log_id = body.get("id")

    if not log_id:
        return error_response(
            "Food log id is required.",
            400
        )

    try:
        food_log = FoodLog.objects.get(id=log_id)
    except FoodLog.DoesNotExist:
        return error_response(
            "Food log not found.",
            404
        )

    food_log.delete()

    return success_response(
        "Food log deleted successfully."
    )

@csrf_exempt
def food_log_api(request):

    if request.method == "GET":
        return get_food_logs(request)
    
    elif request.method == "POST":
        return create_food_log(request)
    
    elif request.method == "PUT":
        return update_food_log(request)
    
    elif request.method == "DELETE":
        return delete_food_log(request)
    
    return error_response(
        "Method not allowed",
        405
    )

# ============================
# MEDICAL PROFILE API
# ============================

def get_medical_profile(request):
    """
    Get a medical profile.

    Temporary implementation:
    Currently uses `profile_id` from the query parameter because
    authentication has not been implemented yet.

    TODO:
    Replace `profile_id` with the authenticated user's medical profile
    after JWT/session authentication is implemented.
    """

    profile_id = request.GET.get("profile_id")

    if not profile_id:
        return error_response(
            "Profile ID is required.",
            400
        )

    try:
        medical_profile = MedicalProfile.objects.get(id=profile_id)
    except MedicalProfile.DoesNotExist:
        return error_response(
            "Medical profile not found.",
            404
        )

    return JsonResponse({
        "id": medical_profile.id,
        "user_id": medical_profile.user_id,
        "full_name": medical_profile.fullName,
        "diabetes_type": medical_profile.diabetesType,
        "target_sugar_low": medical_profile.targetSugarLow,
        "target_sugar_high": medical_profile.targetSugarHigh,
        "birth_date": medical_profile.birthDate,
        "weight_kg": medical_profile.weightKg,
    })

def update_medical_profile(request):
    """
    Update a medical profile.

    Temporary implementation:
    Currently updates a medical profile using the provided profile ID.

    TODO:
    Replace the profile ID with the authenticated user's medical profile
    after authentication is implemented.
    """

    body, error = parse_json_body(request)

    if error:
        return error

    profile_id = body.get("id")
    full_name = body.get("full_name")
    diabetes_type = body.get("diabetes_type")
    target_sugar_low = body.get("target_sugar_low")
    target_sugar_high = body.get("target_sugar_high")
    birth_date = body.get("birth_date")
    weight_kg = body.get("weight_kg")

    if not all([
        profile_id,
        full_name,
        diabetes_type,
        target_sugar_low,
        target_sugar_high,
        birth_date,
        weight_kg,
    ]):
        return error_response(
            "All fields are required.",
            400
        )

    try:
        medical_profile = MedicalProfile.objects.get(id=profile_id)
    except MedicalProfile.DoesNotExist:
        return error_response(
            "Medical profile not found.",
            404
        )

    medical_profile.fullName = full_name
    medical_profile.diabetesType = diabetes_type
    medical_profile.targetSugarLow = target_sugar_low
    medical_profile.targetSugarHigh = target_sugar_high
    medical_profile.birthDate = birth_date
    medical_profile.weightKg = weight_kg

    medical_profile.save()

    return success_response(
        "Medical profile updated successfully."
    )
        
@csrf_exempt
def medical_profile_api(request):

    if request.method == "GET":
        return get_medical_profile(request)

    elif request.method == "PUT":
        return update_medical_profile(request)

    return error_response(
        "Method not allowed.",
        405
    )