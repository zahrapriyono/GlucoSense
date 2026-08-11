from django.shortcuts import render

def list_doctors(request):
    doctors = [
        {
            'photo': 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=120&h=120&fit=crop&crop=face',
            'name': 'Dr. Sarah Chen, MD',
            'specialty': 'ENDOCRINOLOGIST',
            'hospital': 'Metabolic Health Institute, NY',
            'availability': 'Tomorrow, 9:00 AM',
            'insurance': 'Accepts most major insurance',
            'rating': 4.9, 'reviews': 128,
        },
        {
            'photo': 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=120&h=120&fit=crop&crop=face',
            'name': 'Marcus Thorne, RD',
            'specialty': 'CLINICAL DIETITIAN',
            'hospital': 'Vitality Nutrition Center, Virtual',
            'availability': 'Wed, May 15',
            'insurance': 'Telehealth only',
            'rating': 4.8, 'reviews': 84,
        },
        {
            'photo': 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=120&h=120&fit=crop&crop=face',
            'name': 'Dr. James Wilson, MD',
            'specialty': 'ENDOCRINOLOGIST',
            'hospital': 'St. Mary Medical Center, NJ',
            'availability': 'Friday, 11:30 AM',
            'insurance': 'Accepts most major insurance',
            'rating': 5.0, 'reviews': 210,
        },
        {
            'photo': 'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=120&h=120&fit=crop&crop=face',
            'name': 'Elena Rodriguez, MS',
            'specialty': 'NUTRITIONIST',
            'hospital': 'Precision Wellness, CT',
            'availability': 'Next Monday',
            'insurance': 'Out-of-network provider',
            'rating': 4.7, 'reviews': 52,
        },
    ]
    return render(request, 'doctors/list.html', {'doctors': doctors, 'total': 42})