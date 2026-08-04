from django.shortcuts import render

def list_doctors(request):
    doctors = [
        {
            'name': 'Dr. Sarah Chen, MD',
            'specialty': 'ENDOCRINOLOGIST',
            'hospital': 'Metabolic Health Institute, NY',
            'availability': 'Tomorrow, 9:00 AM',
            'insurance': 'Accepts most major insurance',
            'rating': 4.9, 'reviews': 128,
        },
        {
            'name': 'Marcus Thorne, RD',
            'specialty': 'CLINICAL DIETITIAN',
            'hospital': 'Vitality Nutrition Center, Virtual',
            'availability': 'Wed, May 15',
            'insurance': 'Telehealth only',
            'rating': 4.8, 'reviews': 94,
        },
        {
            'name': 'Dr. James Wilson, MD',
            'specialty': 'ENDOCRINOLOGIST',
            'hospital': 'St. Mary Medical Center, NJ',
            'availability': 'Friday, 11:30 AM',
            'insurance': 'Accepts most major insurance',
            'rating': 5.0, 'reviews': 210,
        },
    ]
    return render(request, 'doctors/list.html', {'doctors': doctors})