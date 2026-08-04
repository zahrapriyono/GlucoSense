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
        data = json.load(request.body)
        form_data = convert_to_model_format(data)
        prediction = predict_risk(form_data)
        return JsonResponse(prediction)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def convert_to_model_format(data):
    """Konversi input form HTMl ke 21 fitur BRFSS untuk model."""
    age_years = int(data.get('age', 45))

    # Konvesi umur ke kategori BRFS (1-13)
    age_map = [(24,1),(29,2),(34,3),(39,4),(44,5),(49,6),
               (54,7),(59,8),(64,9),(69,10),(74,11),(79,12)]
    age_cat = 13
    for max_age, cat in age_map:
        if age_years <= max_age:
            age_cat = cat
            break

    # Hitung BMI dari weight dan height
    weight_kg = float(data.get('weight', 70))
    height_cm = float(data.get('height', 170))
    bmi = round(weight_kg/ ((height_cm / 100) ** 2), 1)

    # Activity level ke binary PhysActivity
    activity = data.get('activity_level', 'moderate')
    phys_activity = 0 if activity == 'sedentary' else 1

    # Blood pressure ke binary HighBP
    systolic = data.get('systolic_bp', 120)
    diastolic = data.get('diastolic_bp', 80)
    high_bp = 1 if (systolic >= 140 or diastolic >90) else 0

    return {
        'HighBP': high_bp,
        'HighChol': int(data.get('high_col', 0)),
        'CholCheck': int(data.get('chol_check', 1)),
        'BMI': bmi,
        'Smoker': int(data.get('smoker', 0)),
        'Stroke': int(data.get('stroke', 0)),
        'HeartDiseaseAttack': int(data.get('heart_disease', 0)),
        'PhysActivity': phys_activity,
        'Fruits': int(data.get('fruits', 1)),
        'Veggies': int(data.get('veggies', 1)),
        'HvyAlcoholConsump': int(data.get('heavy_alcohhol', 0)),
        'AnyHealthcare': int(data.get('any_healthcare', 1)),
        'NoDocbcCost': int(data.get('no_doc_cost', 0)),
        'GenHlth': int(data.get('gen_health', 3)),
        'MentHlth': int(data.get('mental_health_days', 0)),
        'PhysHlth': int(data.get('physical_health_days', 0)),
        'DiffWalk': int(data.get('diff_walk', 0)),
        'Sex': int(data.get('sex', 0)),
        'Age': age_cat,
        'Education': int(data.get('education', 4)),
        'Income': int(data.get('income', 5)),
    }