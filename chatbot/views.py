import requests
import os
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from core_api.auth import verify_token
from core_api.models import ChatHistory
from core_api.utils import get_medical_profile

AI_SERVICE_URL = os.getenv('AI_SERVICE_URL', 'http://localhost:8001')


@csrf_exempt
def chat(request):
    if request.method == 'GET':
        return render(request, 'chatbot/chat.html')

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')

        response = requests.post(
            f"{AI_SERVICE_URL}/chat/",
            json={"message": user_message},
            timeout=30
        )
        result = response.json()
        ai_response = result.get('answer', '')

        # Simpan ke ChatHistory jika token valid
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            payload = verify_token(token)

            if payload is not None:
                try:
                    user = User.objects.get(id=payload['user_id'])
                    medical_profile = get_medical_profile(user)
                    if medical_profile is not None:
                        ChatHistory.objects.create(
                            medicalProfile=medical_profile,
                            userMessage=user_message,
                            aiResponse=ai_response,
                        )
                except User.DoesNotExist:
                    pass

        return JsonResponse(result)

    except requests.exceptions.ConnectionError:
        return JsonResponse({
            'answer': 'AI service is currently unavailable. Please try again later.',
            'sources': []
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)