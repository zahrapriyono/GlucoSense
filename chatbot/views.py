from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .rag import get_response


@csrf_exempt  # Untuk development — nanti pakai CSRF token di production
@require_http_methods(["POST"])
def chat_api(request):
    """
    API endpoint untuk chatbot.
    
    Request body (JSON):
        {"message": "apa itu diabetes tipe 2?"}
    
    Response (JSON):
        {
            "answer": "...",
            "sources": [...],
            "query": "..."
        }
    """
    try:
        body = json.loads(request.body)
        message = body.get('message', '').strip()
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        if len(message) > 500:
            return JsonResponse({'error': 'Message too long (max 500 characters)'}, status=400)
        
        # Panggil RAG pipeline
        result = get_response(message)
        
        return JsonResponse(result)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
