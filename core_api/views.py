from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from assessment.ml.predictor import predict_risk
from datetime import datetime
from .auth import (generate_token, jwt_required)
from .utils import (
    parse_json_body,
    success_response,
    error_response,
    validate_required_fields,
    get_medical_profile,
)

from .models import (
    Article,
    Doctor,
    MedicalProfile,
    BloodGlucoseLog,
    FoodLog,
    FavoriteDoctor,
    ChatHistory,
)

from chatbot.rag import get_response

# ==============================
# ARTICLE API
# ==============================

def get_article_list(request):
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
        
    return success_response(
        message="Articles retrieved successfully.",
        data=data,
        status=200
    )

def get_article_detail(request, article_id):

    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        return error_response(
            "Article not found.",
            status=404
        )

    return success_response(
        message="Article retrieved successfully.",
        data={
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "category": article.category,
            "thumbnail_url": article.thumbnailUrl,
            "created_at": article.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
        },
        status=200
    )


# ========================
# DOCTOR API
# ========================

def get_doctor_list(request):
    city_filter = request.GET.get('city')
    experience_filter = request.GET.get('experience')
    
    doctors = Doctor.objects.all().order_by('createdAt')
    
    if city_filter:
        doctors = doctors.filter(city__iexact=city_filter)
        
    if experience_filter:
        try:
            experience_filter = int(experience_filter)
        except ValueError:
            return error_response(
                "Experience must be a valid number.",
                status=400
            )

        doctors = doctors.filter(
            experienceYears__gte=experience_filter
        )
            
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
        
    return success_response(
        message="Doctors retrieved successfully.",
        data=data,
        status=200
    )

def get_doctor_detail(request, doctor_id):

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return error_response(
            "Doctor not found.",
            status=404
        )

    return success_response(
        message="Doctor retrieved successfully.",
        data={
            "id": doctor.id,
            "full_name": doctor.fullName,
            "specialization": doctor.specialization,
            "city": doctor.city,
            "experience_years": doctor.experienceYears,
            "description": doctor.description,
            "profile_picture_url": doctor.profilePictureUrl,
        },
        status=200
    )

# =========================
# BLOOD GLUCOSE API
# =========================

def get_glucose_logs(request):

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    logs = BloodGlucoseLog.objects.filter(
        medicalProfile=medical_profile
    ).order_by("loggedAt")
   
    data = []

    for log in logs:
        data.append({
            'id': log.id,
            'medical_profile_id': log.medicalProfile_id,
            'sugar_level': log.sugarLevel,
            'log_context': log.logContext,
            'logged_at': log.loggedAt.strftime('%Y-%m-%d %H:%M:%S'),
        })

    return success_response(
        message="Blood glucose logs retrieved successfully.",
        data=data,
        status=200
    )

def create_glucose_log(request):
    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    required_fields = [
        "sugar_level",
        "log_context",
        "logged_at",
    ]

    missing_fields = validate_required_fields(
        body,
        required_fields,
    )

    if missing_fields:
        return error_response(
            f"Missing required fields: {', '.join(missing_fields)}",
            status=400
        )

    try:
        sugar_level = float(body.get("sugar_level"))
    except (TypeError, ValueError):
        return error_response(
            "Sugar level must be a valid number.",
            status=400
        )

    if sugar_level <= 0:
        return error_response(
            "Sugar level must be greater than 0.",
            status=400
        )
    
    log_context = body.get("log_context")
    logged_at = body.get("logged_at")

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    glucose_log = BloodGlucoseLog.objects.create(
        medicalProfile=medical_profile,
        sugarLevel=sugar_level,
        logContext=log_context,
        loggedAt=logged_at,
    )
    return success_response(
        message="Blood glucose log created successfully",
        status=201,
        id=glucose_log.id
    )

def update_glucose_log(request):
    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    required_fields = [
        "log_id",
        "sugar_level",
        "log_context",
        "logged_at",
    ]

    missing_fields = validate_required_fields(
        body,
        required_fields,
    )

    if missing_fields:
        return error_response(
            f"Missing required fields: {', '.join(missing_fields)}",
            status=400
        )

    log_id = body.get("log_id")

    try:
        sugar_level = float(body.get("sugar_level"))
    except (TypeError, ValueError):
        return error_response(
            "Sugar level must be a valid number.",
            status=400
        )

    if sugar_level <= 0:
        return error_response(
            "Sugar level must be greater than 0.",
            status=400
        )
    
    log_context = body.get("log_context")
    logged_at = body.get("logged_at")

    try:
        logged_at = datetime.strptime(
            logged_at,
            "%Y-%m-%d %H:%M:%S"
        )
    except (TypeError, ValueError):
        return error_response(
            "Logged at must use format YYYY-MM-DD HH:MM:SS.",
            status=400
        )

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    try:
        glucose_log = BloodGlucoseLog.objects.get(
            id=log_id,
            medicalProfile=medical_profile,
        )
    except BloodGlucoseLog.DoesNotExist:
        return error_response(
            "Blood glucose log not found.",
            status=404
        )

    glucose_log.sugarLevel = sugar_level
    glucose_log.logContext = log_context
    glucose_log.loggedAt = logged_at

    glucose_log.save()

    return success_response(
        message="Blood glucose log updated successfully.",
        data={
            "id": glucose_log.id,
            "medical_profile_id": glucose_log.medicalProfile_id,
            "sugar_level": glucose_log.sugarLevel,
            "log_context": glucose_log.logContext,
            "logged_at": glucose_log.loggedAt.strftime("%Y-%m-%d %H:%M:%S"),
        },
        status=200
    )

def delete_glucose_log(request):
    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    required_fields = [
        "log_id",
    ]

    missing_fields = validate_required_fields(
        body,
        required_fields,
    )

    if missing_fields:
        return error_response(
            f"Missing required fields: {', '.join(missing_fields)}",
            status=400
        )

    log_id = body.get("log_id")

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )
    
    try:
        glucose_log = BloodGlucoseLog.objects.get(
            id=log_id,
            medicalProfile=medical_profile,
        )
    except BloodGlucoseLog.DoesNotExist:
        return error_response(
            "Blood glucose log not found.",
            status=404
        )

    glucose_log.delete()

    return success_response(
        message="Blood glucose log deleted successfully.",
        status=200
    )

@csrf_exempt
@jwt_required
def glucose_log_api(request):

    if request.method == 'GET':
        return get_glucose_logs(request)
    
    elif request.method == "POST":
        return create_glucose_log(request)
    
    elif request.method == "PUT":
        return update_glucose_log(request)
    
    elif request.method == "DELETE":
        return delete_glucose_log(request)
    
    return error_response(
        "Method not allowed.",
        status=405
    )

# ===========================
# FOOD LOG API
# ===========================

def get_food_logs(request):

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    logs = FoodLog.objects.filter(
        medicalProfile=medical_profile
    ).order_by("loggedAt")

    data = []

    for log in logs:
        data.append(
            {
                "id": log.id,
                "food_name": log.foodName,
                "estimated_carbs": log.estimatedCarbs,
                "logged_at": log.loggedAt.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return success_response(
        message="Food logs retrieved successfully.",
        data=data,
        status=200
    )

def create_food_log(request):
    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    required_fields = [
        "food_name",
        "estimated_carbs",
        "logged_at",
    ]

    missing_fields = validate_required_fields(
        body,
        required_fields,
    )

    if missing_fields:
        return error_response(
            f"Missing required fields: {', '.join(missing_fields)}",
            status=400
        )

    food_name = body.get("food_name")

    try:
        estimated_carbs = float(body.get("estimated_carbs"))
    except (TypeError, ValueError):
        return error_response(
            "Estimated carbohydrates must be a valid number.",
            status=400
        )

    if estimated_carbs <= 0:
        return error_response(
            "Estimated carbohydrates must be greater than 0.",
            status=400
        )
    
    logged_at = body.get("logged_at")

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    food_log = FoodLog.objects.create(
        medicalProfile=medical_profile,
        foodName=food_name,
        estimatedCarbs=estimated_carbs,
        loggedAt=logged_at,
    )

    return success_response(
        message="Food log created successfully.",
        status=201,
        id=food_log.id,
    )

def update_food_log(request):
    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    required_fields = [
        "log_id",
        "food_name",
        "estimated_carbs",
        "logged_at",
    ]

    missing_fields = validate_required_fields(
        body,
        required_fields,
    )

    if missing_fields:
        return error_response(
            f"Missing required fields: {', '.join(missing_fields)}",
            status=400
        )

    log_id = body.get("log_id")
    food_name = body.get("food_name")

    try:
        estimated_carbs = float(body.get("estimated_carbs"))
    except (TypeError, ValueError):
        return error_response(
            "Estimated carbohydrates must be a valid number.",
            status=400
        )

    if estimated_carbs <= 0:
        return error_response(
            "Estimated carbohydrates must be greater than 0.",
            status=400
        )
    
    logged_at = body.get("logged_at")

    try:
        logged_at = datetime.strptime(
            logged_at,
            "%Y-%m-%d %H:%M:%S"
        )
    except (TypeError, ValueError):
        return error_response(
            "Logged at must use format YYYY-MM-DD HH:MM:SS.",
            status=400
        )

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    try:
        food_log = FoodLog.objects.get(
            id=log_id,
            medicalProfile=medical_profile
        )
    except FoodLog.DoesNotExist:
        return error_response(
            "Food log not found.",
            status=404
        )

    food_log.foodName = food_name
    food_log.estimatedCarbs = estimated_carbs
    food_log.loggedAt = logged_at

    food_log.save()

    return success_response(
        message="Food log updated successfully.",
        data={
            "id": food_log.id,
            "food_name": food_log.foodName,
            "estimated_carbs": food_log.estimatedCarbs,
            "logged_at": food_log.loggedAt.strftime("%Y-%m-%d %H:%M:%S"),
        },
        status=200
    )
    
def delete_food_log(request):
    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    required_fields = [
        "log_id"
    ]

    missing_fields = validate_required_fields(
        body,
        required_fields
    )

    if missing_fields:
        return error_response(
            f"Missing required fields: {', '.join(missing_fields)}",
            status=400
        )

    log_id = body.get("log_id")

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    try:
        food_log = FoodLog.objects.get(
            id=log_id,
            medicalProfile=medical_profile
        )
    except FoodLog.DoesNotExist:
        return error_response(
            "Food log not found.",
            status=404
        )

    food_log.delete()

    return success_response(
        message="Food log deleted successfully.",
        status=200
    )

@csrf_exempt
@jwt_required
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
        status=405
    )

# ============================
# MEDICAL PROFILE API
# ============================

def get_medical_profile_api(request):
    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    return success_response(
        message="Medical profile retrieved successfully.",
        data={
            "id": medical_profile.id,
            "user_id": medical_profile.user_id,
            "full_name": medical_profile.fullName,
            "diabetes_type": medical_profile.diabetesType,
            "target_sugar_low": medical_profile.targetSugarLow,
            "target_sugar_high": medical_profile.targetSugarHigh,
            "birth_date": medical_profile.birthDate,
            "weight_kg": medical_profile.weightKg,
            "email": request.user.email,
            "member_since": request.user.date_joined.strftime("%B %Y"),
        },
        status=200
    )

def update_medical_profile(request):
    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    required_fields = [
        "full_name",
        "diabetes_type",
        "target_sugar_low",
        "target_sugar_high",
        "birth_date",
        "weight_kg",
    ]

    missing_fields = validate_required_fields(
        body,
        required_fields,
    )

    if missing_fields:
        return error_response(
            f"Missing required fields: {', '.join(missing_fields)}",
            status=400
        )

    full_name = body.get("full_name")
    diabetes_type = body.get("diabetes_type")
    target_sugar_low = body.get("target_sugar_low")
    target_sugar_high = body.get("target_sugar_high")
    birth_date = body.get("birth_date")
    weight_kg = body.get("weight_kg")

    try:
        target_sugar_low = float(target_sugar_low)
        target_sugar_high = float(target_sugar_high)
        weight_kg = float(weight_kg)
    except (TypeError, ValueError):
        return error_response(
            "Target sugar and weight must be valid numbers.",
            status=400
        )

    if target_sugar_low <= 0:
        return error_response(
            "Target sugar low must be greater than 0.",
            status=400
        )

    if target_sugar_high <= 0 or target_sugar_high <= target_sugar_low:
        return error_response(
            "Target sugar high must be greater than 0 and greater than target sugar low.",
            status=400
        )

    if weight_kg <= 0:
        return error_response(
            "Weight must be greater than 0.",
            status=400
        )

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    medical_profile.fullName = full_name
    medical_profile.diabetesType = diabetes_type
    medical_profile.targetSugarLow = target_sugar_low
    medical_profile.targetSugarHigh = target_sugar_high
    medical_profile.birthDate = birth_date
    medical_profile.weightKg = weight_kg

    medical_profile.save()

    return success_response(
        message="Medical profile updated successfully.",
        status=200
    )
        
@csrf_exempt
@jwt_required
def medical_profile_api(request):

    if request.method == "GET":
        return get_medical_profile_api(request)

    elif request.method == "PUT":
        return update_medical_profile(request)

    return error_response(
        "Method not allowed.",
        status=405
    )

# ============================
# FAVORITE DOCTOR API
# ============================

def get_favorite_doctor(request):

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    favorite_doctors = FavoriteDoctor.objects.filter(medicalProfile=medical_profile).select_related("doctor")

    data = []

    for favorite in favorite_doctors:

        doctor = favorite.doctor

        data.append({
            "id": favorite.id,
            "doctor_id": doctor.id,
            "full_name": doctor.fullName,
            "specialization": doctor.specialization,
            "city": doctor.city,
            "experience_years": doctor.experienceYears,
            "profile_picture_url": doctor.profilePictureUrl,
            "created_at": favorite.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return success_response(
        message="Favorite doctors retrieved successfully.",
        data=data,
        status=200
    )

def add_favorite_doctor(request):
    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    required_fields = [
        "doctor_id",
    ]

    missing_fields = validate_required_fields(
        body,
        required_fields,
    )

    if missing_fields:
        return error_response(
            f"Missing required fields: {', '.join(missing_fields)}",
            status=400
        )

    doctor_id = body.get("doctor_id")

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return error_response(
            "Doctor not found.",
            status=404
        )

    if FavoriteDoctor.objects.filter(
        medicalProfile=medical_profile,
        doctor=doctor
    ).exists():
        return error_response(
            "Doctor is already in favorites.",
            status=409
        )

    FavoriteDoctor.objects.create(
        medicalProfile=medical_profile,
        doctor=doctor,
    )

    return success_response(
        message="Doctor added to favorites successfully.",
        status=201
    )

def delete_favorite_doctor(request):

    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    required_fields = [
        "doctor_id"
    ]

    missing_fields = validate_required_fields(
        body,
        required_fields,
    )

    if missing_fields:
        return error_response(
            f"Missing required fields: {', '.join(missing_fields)}",
            status=400
        )

    doctor_id = body.get("doctor_id")

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    try:
        favorite_doctor = FavoriteDoctor.objects.get(
            medicalProfile_id = medical_profile,
            doctor_id = doctor_id
        )
    except FavoriteDoctor.DoesNotExist:
        return error_response(
            "Favorite doctor not found.",
            status=404
        )

    favorite_doctor.delete()

    return success_response(
        message="Doctor removed from favorites successfully.",
        status=200
    )

@csrf_exempt
@jwt_required
def favorite_doctor_api(request):

    if request.method == "GET":
        return get_favorite_doctor(request)
    
    elif request.method == "POST":
        return add_favorite_doctor(request)
    
    elif request.method == "DELETE":
        return delete_favorite_doctor(request)

    return error_response(
        "Method not allowed.",
        status=405
    )

# ============================
# CHAT HISTORY API
# ============================

def get_chat_history(request):

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    chat_histories = ChatHistory.objects.filter(
        medicalProfile=medical_profile
    ).order_by("createdAt")

    data = []

    for chat in chat_histories:
        data.append({
            "id": chat.id,
            "user_message": chat.userMessage,
            "ai_response": chat.aiResponse,
            "created_at": chat.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return success_response(
        message="Chat history retrieved successfully.",
        data=data,
        status=200
    )

def send_chat(request):
    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    required_fields = [
        "user_message",
    ]

    missing_fields = validate_required_fields(
        body,
        required_fields,
    )

    if missing_fields:
        return error_response(
            f"Missing required fields: {', '.join(missing_fields)}",
            status=400
        )

    user_message = body.get("user_message")
    ai_response = get_response(user_message)

    medical_profile = get_medical_profile(request.user)

    if medical_profile is None:
        return error_response(
            "Medical profile not found.",
            status=404
        )

    ChatHistory.objects.create(
        medicalProfile=medical_profile,
        userMessage=user_message,
        aiResponse=ai_response,
    )

    return success_response(
        message="Chat history saved successfully.",
        data={
            "user_message": user_message,
            "ai_response": ai_response,
        },
        status=201
    )

@csrf_exempt
@jwt_required
def chat_history_api(request):

    if request.method == "GET":
        return get_chat_history(request)

    return error_response(
        "Method not allowed.",
        status=405
    )

@csrf_exempt
@jwt_required
def chat_api(request):

    if request.method == "POST":
        return send_chat(request)

    return error_response(
        "Method not allowed.",
        status=405
    )

# ============================
# AUTHENTICATION API
# ============================

@csrf_exempt
def register_api(request):

    if request.method != "POST":
        return error_response(
            "Method not allowed.",
            status=405
        )

    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    required_fields = [
        "username",
        "email",
        "password",
        "full_name",
        "diabetes_type",
    ]

    missing_fields = validate_required_fields(
        body,
        required_fields,
    )

    if missing_fields:
        return error_response(
            f"Missing required fields: {', '.join(missing_fields)}",
            status=400
        )

    username = body.get("username")
    email = body.get("email")
    password = body.get("password")
    full_name = body.get("full_name")
    diabetes_type = body.get("diabetes_type")

    if User.objects.filter(username=username).exists():
        return error_response(
            "Username already exists."
        )

    if User.objects.filter(email=email).exists():
        return error_response(
            "Email already exists."
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    MedicalProfile.objects.create(
        user=user,
        fullName=full_name,
        diabetesType=diabetes_type,
    )

    return success_response(
        message="User registered successfully.",
        status=201
    )

@csrf_exempt
def login_api(request):

    if request.method != "POST":
        return error_response(
            "Method not allowed.",
            status=405
        )

    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    required_fields = [
        "email",
        "password",
    ]

    missing_fields = validate_required_fields(
        body,
        required_fields,
    )

    if missing_fields:
        return error_response(
            f"Missing required fields: {', '.join(missing_fields)}",
            status=400
        )

    email = body.get("email")
    password = body.get("password")

    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        user_obj = None

    if user_obj is None:
        return error_response(
            "Invalid email or password.",
            status=401
        )

    user = authenticate(
        username = user_obj.username,
        password=password,
    )

    if user is None:
        return error_response(
            "Invalid username or password.",
            status=401
        )

    token = generate_token(user)

    medical_profile = MedicalProfile.objects.get(user=user)

    return success_response(
        message="Login successful.",
        data={
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "medical_profile": {
                "id": medical_profile.id,
                "full_name": medical_profile.fullName,
                "diabetes_type": medical_profile.diabetesType,
            },
        },
        status=200
    )

def convert_to_model_format(data):
    """Konversi input form HTML ke 21 fitur BRFSS untuk model."""
    age_years = int(data.get('age', 45) or 45)

    # Konversi umur ke kategori BRFSS (1-13)
    age_map = [(24,1),(29,2),(34,3),(39,4),(44,5),(49,6),
               (54,7),(59,8),(64,9),(69,10),(74,11),(79,12)]
    age_cat = 13
    for max_age, cat in age_map:
        if age_years <= max_age:
            age_cat = cat
            break

    # Hitung BMI dari weight dan height
    weight_kg = float(data.get('weight', 70) or 70)
    height_cm = float(data.get('height', 170) or 170)
    bmi = round(weight_kg / ((height_cm / 100) ** 2), 1)

    # Activity level ke binary PhysActivity
    activity = data.get('activity_level', 'moderate')
    phys_activity = 0 if activity == 'sedentary' else 1

    # Blood pressure ke binary HighBP
    # FIX: field name sesuai form (bp_systolic / bp_diastolic) + int conversion
    systolic  = int(data.get('bp_systolic', 120) or 120)
    diastolic = int(data.get('bp_diastolic', 80) or 80)
    high_bp   = 1 if (systolic >= 140 or diastolic >= 90) else 0

    return {
        'HighBP':               high_bp,
        'HighChol':             int(data.get('high_cholesterol', 0) or 0),   # FIX: high_col → high_cholesterol
        'CholCheck':            int(data.get('cholesterol_check_5yr', 1) or 1), # FIX: chol_check → cholesterol_check_5yr
        'BMI':                  bmi,
        'Smoker':               int(data.get('smoking_status', 0) or 0),     # FIX: smoker → smoking_status
        'Stroke':               int(data.get('stroke', 0) or 0),
        'HeartDiseaseorAttack': int(data.get('heart_disease', 0) or 0),      # FIX: typo HeartDiseaseAttack
        'PhysActivity':         phys_activity,
        'Fruits':               int(data.get('eat_fruits', 1) or 1),         # FIX: fruits → eat_fruits
        'Veggies':              int(data.get('eat_vegetables', 1) or 1),     # FIX: veggies → eat_vegetables
        'HvyAlcoholConsump':    int(data.get('heavy_alcohol', 0) or 0),      # FIX: typo heavy_alcohhol
        'AnyHealthcare':        int(data.get('health_insurance', 1) or 1),   # FIX: any_healthcare → health_insurance
        'NoDocbcCost':          int(data.get('skipped_doctor_cost', 0) or 0), # FIX: no_doc_cost → skipped_doctor_cost
        'GenHlth':              int(data.get('general_health', 3) or 3),     # FIX: gen_health → general_health
        'MentHlth':             int(data.get('poor_mental_health_days', 0) or 0),   # FIX field name
        'PhysHlth':             int(data.get('poor_physical_health_days', 0) or 0), # FIX field name
        'DiffWalk':             int(data.get('difficulty_walking', 0) or 0), # FIX: diff_walk → difficulty_walking
        'Sex':                  int(data.get('sex', 0) or 0),
        'Age':                  age_cat,
        'Education':            int(data.get('education_level', 4) or 4),    # FIX: education → education_level
        'Income':               int(data.get('income_level', 5) or 5),       # FIX: income → income_level
    }

@csrf_exempt
@jwt_required
def submit_assessment_api(request):
    print("ASSESSMENT API CALLED")
    
    if request.method != 'POST':
        return error_response(
            message="Method not allowed.",
            status=405
        )

    body = parse_json_body(request)

    if isinstance(body, JsonResponse):
        return body

    form_data = convert_to_model_format(body)

    prediction = predict_risk(form_data)

    return success_response(
        message="Assessment completed successfully.",
        data=prediction,
        status=200
    )