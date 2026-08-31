import requests
import os
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import ChatHistory
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

        # Simpan ke ChatHistory
        medical_profile = get_medical_profile(request.user)
        if medical_profile is not None:
            ChatHistory.objects.create(
                medicalProfile=medical_profile,
                userMessage=user_message,
                aiResponse=ai_response,
            )

        return JsonResponse(result)

    except requests.exceptions.ConnectionError:
        return JsonResponse({
            'answer': 'AI service is currently unavailable. Please try again later.',
            'sources': []
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)