from django.http.response import JsonResponse
from django.shortcuts import redirect


def health(request):
    return JsonResponse({"status": "🟢 OK"})
