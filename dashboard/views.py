from django.shortcuts import render

def profile(request):
    user_data = {
        'name': 'Alex Johnson',
        'member_since': 'Oct 2023',
        'total_assessments': 12,
        'saved_resources': 48,
        'last_assessment': 'March 14, 2024',
        'recent_assessments': [
            {'id': 1, 'date': 'March 14, 2024', 'tier': 'Low Risk',
             'level': 1, 'status': 'Optimal range'},
            {'id': 2, 'date': 'January 02, 2024', 'tier': 'Moderate Risk',
             'level': 2, 'status': 'Needs attention'},
        ]
    }
    return render(request, 'dashboard/profile.html', {'user': user_data})

def report_detail(request, report_id):
    # Dummy data — nanti di-replace dengan query ke Assessment model
    reports = {
        1: {
            'id': 1,
            'date': 'March 14, 2024',
            'tier': 'Low Risk',
            'level': 1,
            'probability': 23,
            'status': 'Optimal range',
            'risk_factors': [
                {'name': 'BMI', 'value': '22.4', 'status': 'normal', 'note': 'Within healthy range'},
                {'name': 'Blood Pressure', 'value': '118/76 mmHg', 'status': 'normal', 'note': 'Normal'},
                {'name': 'Physical Activity', 'value': 'Moderate', 'status': 'normal', 'note': '3–5 hrs/week'},
                {'name': 'General Health', 'value': 'Very Good', 'status': 'normal', 'note': 'Self-reported'},
                {'name': 'Cholesterol Check', 'value': 'Yes', 'status': 'normal', 'note': 'Within 5 years'},
                {'name': 'Smoking', 'value': 'Non-smoker', 'status': 'normal', 'note': 'No risk'},
            ],
            'recommendations': [
                'Maintain your current exercise routine of 3–5 hours per week.',
                'Continue eating fruits and vegetables daily.',
                'Schedule a routine cholesterol check in the next 12 months.',
                'Monitor blood pressure monthly.',
            ],
        },
        2: {
            'id': 2,
            'date': 'January 02, 2024',
            'tier': 'Moderate Risk',
            'level': 2,
            'probability': 51,
            'status': 'Needs attention',
            'risk_factors': [
                {'name': 'BMI', 'value': '27.8', 'status': 'warning', 'note': 'Slightly above healthy range'},
                {'name': 'Blood Pressure', 'value': '138/88 mmHg', 'status': 'warning', 'note': 'Pre-hypertension'},
                {'name': 'Physical Activity', 'value': 'Sedentary', 'status': 'danger', 'note': 'Less than 1 hr/week'},
                {'name': 'General Health', 'value': 'Good', 'status': 'normal', 'note': 'Self-reported'},
                {'name': 'High Cholesterol', 'value': 'Yes', 'status': 'warning', 'note': 'Reported'},
                {'name': 'Smoking', 'value': 'Former smoker', 'status': 'warning', 'note': 'Residual risk'},
            ],
            'recommendations': [
                'Consult a doctor about your blood pressure readings.',
                'Aim to increase physical activity to at least 150 minutes per week.',
                'Consider a dietary review with a registered dietitian.',
                'Recheck cholesterol levels within 3 months.',
            ],
        },
    }
    report = reports.get(report_id, reports[1])
    return render(request, 'dashboard/report_detail.html', {'report': report})