from django.http.response import JsonResponse


def health(request):
    return JsonResponse({"status": "🟢 OK"})
