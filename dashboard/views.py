from django.shortcuts import render

def profile(request):
    return render(request, 'dashboard/profile.html')

def report_detail(request, report_id):
    return render(
        request,
        'dashboard/report_detail.html',
        {'report_id': report_id}
    )
