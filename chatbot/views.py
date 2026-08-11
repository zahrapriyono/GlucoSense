from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .rag import get_response

def chat(request):
    return render(request, 'chatbot/chat.html')

@csrf_exempt
def api_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')

        from .rag import get_response
        result = get_response(message)

        return JsonResponse({
            'answer': result['answer'],
            'sources': result['sources']
        })

    return JsonResponse({'error': 'Method not allowed'}, status=405)