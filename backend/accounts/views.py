from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
import json

User = get_user_model()

@csrf_exempt
@api_view(['POST'])
def check_email(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        exists = User.objects.filter(email=email).exists()
        return JsonResponse({'available': not exists})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@api_view(['POST'])
def check_nickname(request):
    try:
        data = json.loads(request.body)
        nickname = data.get('nickname')
        exists = User.objects.filter(nickname=nickname).exists()
        return JsonResponse({'available': not exists})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
