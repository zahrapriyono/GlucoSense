import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Article,
    Doctor,
    MedicalProfile,
    BloodGlucoseLog,
    FoodLog,
)


def parse_json_body(request):
    try:
        return json.loads(request.body), None
    except json.JSONDecodeError:
        return None, JsonResponse(
            {
                "error": "Invalid JSON format"
            },
            status=400
        )


def error_response(message, status):
    return JsonResponse(
        {
            "error": message
        },
        status=status
    )


def success_response(message, status=200, **kwargs):
    response = {
        "message": message
    }

    response.update(kwargs)

    return JsonResponse(
        response,
        status=status
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
    """
    Mengambil daftar dokter spesialis dengan fitur pencarian/filter
    berdasarkan kota dan minimal pengalaman kerja.
    """
    # Mengambil parameter filter dari URL (jika ada)
    # Contoh: /api/doctors/?city=jakarta&experience=5
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

# ============================
# MEDICAL PROFILE API
# ============================