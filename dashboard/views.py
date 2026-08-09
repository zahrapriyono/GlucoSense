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
    reports = {
        1: {
            'id': 1,
            'date': 'March 14, 2024',
            'tier': 'Low Risk',
            'level': 1,
            'probability': 23,
            'status': 'Optimal range',
            'risk_factors': [
                {
                    'name': 'BMI',
                    'value': '22.4 (Normal Range)',
                    'label': 'Optimal',       
                    'status': 'optimal',      
                    'bar': 85,                 
                },
                {
                    'name': 'Activity Level',
                    'value': '4+ days/week',
                    'label': 'Active',
                    'status': 'active',
                    'bar': 90,
                },
                {
                    'name': 'Family History',
                    'value': 'No immediate relatives',
                    'label': 'Minimal',
                    'status': 'minimal',
                    'bar': 20,
                },
                {
                    'name': 'Blood Pressure',
                    'value': '125/82 mmHg (Monitor)',
                    'label': 'Elevated',
                    'status': 'elevated',
                    'bar': 65,
                },
            ],
            'recommendations': [
                {'text': 'Maintain your current moderate-to-high activity level.', 'icon': 'check'},
                {'text': 'Continue balanced nutritional choices to support a healthy BMI.', 'icon': 'check'},
                {'text': 'Monitor blood pressure periodically; slight elevation noted.', 'icon': 'warning'},
                {'text': 'Schedule your routine annual screening next year.', 'icon': 'info'},
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
                {
                    'name': 'BMI',
                    'value': '22.4 (Normal Range)',
                    'label': 'Optimal',       
                    'status': 'optimal',      
                    'bar': 85,                 
                },
                {
                    'name': 'Activity Level',
                    'value': '4+ days/week',
                    'label': 'Active',
                    'status': 'active',
                    'bar': 90,
                },
                {
                    'name': 'Family History',
                    'value': 'No immediate relatives',
                    'label': 'Minimal',
                    'status': 'minimal',
                    'bar': 20,
                },
                {
                    'name': 'Blood Pressure',
                    'value': '125/82 mmHg (Monitor)',
                    'label': 'Elevated',
                    'status': 'elevated',
                    'bar': 65,
                },
            ],
            'recommendations': [
                {'text': 'Maintain your current moderate-to-high activity level.', 'icon': 'check'},
                {'text': 'Continue balanced nutritional choices to support a healthy BMI.', 'icon': 'check'},
                {'text': 'Monitor blood pressure periodically; slight elevation noted.', 'icon': 'warning'},
                {'text': 'Schedule your routine annual screening next year.', 'icon': 'info'},
            ],
        },
    }
    report = reports.get(report_id, reports[1])
    return render(request, 'dashboard/report_detail.html', {'report': report})
