from django.shortcuts import render

def profile(request):
    user_data = {
        'name': 'Alex Johnson',
        'member_since': 'Oct 2023',
        'total_assessments': 12,
        'saved_resources': 48,
        'last_assessment': 'March 14, 2024',
        'recent_assessments': [
            {'date': 'March 14, 2024', 'tier': 'Low Risk',
             'level': 1, 'status': 'Optimal range'},
            {'date': 'January 02, 2024', 'tier': 'Moderate Risk',
             'level': 3, 'status': 'Needs attention'},
        ]
    }
    return render(request, 'dashboard/profile.html', {'user': user_data})