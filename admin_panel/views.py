from django.views.generic import ListView
from . import models
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from . import serializers
from django.contrib.gis.measure import Distance
from django.core.serializers import serialize
from rest_framework.decorators import action
from rest_framework_datatables import filters
from rest_framework.response import Response
from rest_framework_datatables.renderers import DatatablesRenderer, JSONRenderer


class NearbyLocationFilterBackend(filters.DatatablesFilterBackend):

    def filter_queryset(self, request, queryset, view):
        nearby_pk = request.query_params.get('nearby_pk', None)
        if nearby_pk is not None:
            point = models.Request.objects.get(pk=nearby_pk).location
            return queryset.filter(location__distance_lt=(point, Distance(km=10))).order_by('pk')
        return queryset


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
    filter_backends = [NearbyLocationFilterBackend]
    renderer_classes = [DatatablesRenderer]


class RequestList(ListView):
    model = models.Request
