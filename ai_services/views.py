from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def HealthCheck(request):
    return JsonResponse({"status": "SUCCESS"})