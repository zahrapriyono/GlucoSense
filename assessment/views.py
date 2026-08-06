from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ml.predictor import predict_risk
import json

def form(request):
    return render(request, 'assessment/form.html')

def result(request):
    return render(request, 'assessment/result.html')

@csrf_exempt
def submit(request):
    if request.method == 'POST':
        data = json.loads(request.body)          # FIX: load → loads
        form_data = convert_to_model_format(data)
        prediction = predict_risk(form_data)
        return JsonResponse(prediction)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

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