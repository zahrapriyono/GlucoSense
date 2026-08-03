import json

from django.http import JsonResponse
from .models import MedicalProfile

def parse_json_body(request):
    try:
        return json.loads(request.body)
    
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "error": "Invalid JSON format"
            },
            status=400
        )

def error_response(message, status):
    return JsonResponse(
        {
            "error": message
        },
        status=status
    )


def success_response(message, status=200, **kwargs):
    response = {
        "message": message
    }

    response.update(kwargs)

    return JsonResponse(
        response,
        status=status
    )

def validate_required_fields(data, required_fields):
    missing_fields = []

    for field in required_fields:
        value = data.get(field)

        if value is None or value == "":
            missing_fields.append(field)

    return missing_fields

def get_medical_profile(user):

    try:
        return MedicalProfile.objects.get(user=user)

    except MedicalProfile.DoesNotExist:
        return None