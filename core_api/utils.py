import json

from django.http import JsonResponse

def parse_json_body(request):
    try:
        return json.loads(request.body), None
    except json.JSONDecodeError:
        return None, JsonResponse(
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