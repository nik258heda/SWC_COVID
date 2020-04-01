from django.views.generic import ListView
from . import models
from django.http import JsonResponse
from rest_framework import viewsets
from . import serializers


def approve_request(request):
    try:
        pk = request.GET.get('pk')
        req = models.Request.objects.get(pk=pk)
    except models.Request.DoesNotExist as e:
        return JsonResponse({'error': e})

    req.status_completed = True
    req.save()
    return JsonResponse({'approved': 'True'})


class RequestViewSet(viewsets.ModelViewSet):
    queryset = models.Request.objects.all()
    serializer_class = serializers.RequestSerializer


class RequestList(ListView):
    model = models.Request
