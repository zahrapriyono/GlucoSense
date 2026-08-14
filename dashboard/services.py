def build_assessment_factors(assessment):
    factors = []

    # BMI
    if assessment.bmi < 18.5:
        bmi_label = "Underweight"
        bmi_status = "warning"
    elif assessment.bmi < 25:
        bmi_label = "Optimal"
        bmi_status = "optimal"
    elif assessment.bmi < 30:
        bmi_label = "Overweight"
        bmi_status = "elevated"
    else:
        bmi_label = "Obese"
        bmi_status = "warning"

    factors.append({
        "name": "BMI",
        "value": f"{assessment.bmi:.1f}",
        "label": bmi_label,
        "status": bmi_status,
        "bar": min(int((assessment.bmi / 40) * 100), 100),
    })

    # Physical Activity
    if assessment.physActivity == 1:
        activity_label = "Active"
        activity_status = "active"
        activity_bar = 90
    else:
        activity_label = "Inactive"
        activity_status = "warning"
        activity_bar = 30

    factors.append({
        "name": "Activity Level",
        "value": (
            "Physically active"
            if assessment.physActivity == 1
            else "Not physically active"
        ),
        "label": activity_label,
        "status": activity_status,
        "bar": activity_bar,
    })

    # High Blood Pressure
    if assessment.highBP == 1:
        bp_label = "Elevated"
        bp_status = "elevated"
        bp_bar = 70
        bp_value = "High blood pressure reported"
    else:
        bp_label = "Normal"
        bp_status = "optimal"
        bp_bar = 90
        bp_value = "No high blood pressure reported"

    factors.append({
        "name": "Blood Pressure",
        "value": bp_value,
        "label": bp_label,
        "status": bp_status,
        "bar": bp_bar,
    })

    # Cholesterol
    if assessment.highChol == 1:
        chol_label = "Elevated"
        chol_status = "elevated"
        chol_bar = 65
        chol_value = "High cholesterol reported"
    else:
        chol_label = "Optimal"
        chol_status = "optimal"
        chol_bar = 90
        chol_value = "No high cholesterol reported"

    factors.append({
        "name": "Cholesterol",
        "value": chol_value,
        "label": chol_label,
        "status": chol_status,
        "bar": chol_bar,
    })

    # Smoking
    if assessment.smoker == 1:
        smoking_label = "Risk factor"
        smoking_status = "warning"
        smoking_bar = 30
        smoking_value = "Current smoker"
    else:
        smoking_label = "Low risk"
        smoking_status = "optimal"
        smoking_bar = 90
        smoking_value = "Non-smoker"

    factors.append({
        "name": "Smoking",
        "value": smoking_value,
        "label": smoking_label,
        "status": smoking_status,
        "bar": smoking_bar,
    })

    return factors

def build_assessment_recommendations(assessment):
    recommendations = []

    # Physical activity
    if assessment.physActivity == 0:
        recommendations.append({
            "text": "Consider increasing your regular physical activity.",
            "icon": "warning"
        })
    else:
        recommendations.append({
            "text": "Maintain your current level of physical activity.",
            "icon": "check"
        })

    # Fruits and vegetables
    if assessment.fruits == 0 or assessment.veggies == 0:
        recommendations.append({
            "text": "Consider including more fruits and vegetables in your diet.",
            "icon": "warning"
        })
    else:
        recommendations.append({
            "text": "Continue maintaining a balanced diet with fruits and vegetables.",
            "icon": "check"
        })

    # Smoking
    if assessment.smoker == 1:
        recommendations.append({
            "text": "Consider avoiding smoking to support your overall health.",
            "icon": "warning"
        })
    else:
        recommendations.append({
            "text": "Continue avoiding smoking.",
            "icon": "check"
        })

    # High blood pressure
    if assessment.highBP == 1:
        recommendations.append({
            "text": "Consider monitoring your blood pressure regularly.",
            "icon": "warning"
        })

    # High cholesterol
    if assessment.highChol == 1:
        recommendations.append({
            "text": "Consider discussing your cholesterol levels with a healthcare professional.",
            "icon": "warning"
        })

    # Overall risk
    if assessment.tier == "High":
        recommendations.append({
            "text": "Consider discussing your assessment result with a healthcare professional.",
            "icon": "warning"
        })
    elif assessment.tier == "Moderate":
        recommendations.append({
            "text": "Continue monitoring your health factors and maintaining healthy habits.",
            "icon": "info"
        })
    else:
        recommendations.append({
            "text": "Continue maintaining your healthy lifestyle habits.",
            "icon": "check"
        })

    return recommendations