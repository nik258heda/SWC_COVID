from django.views.generic import ListView
from . import models
from django.http import JsonResponse
from rest_framework import viewsets
from . import serializers
from django.contrib.gis.measure import Distance
from rest_framework_datatables import filters
from rest_framework_datatables.renderers import DatatablesRenderer
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View
from django.db.models import Count
from django.shortcuts import render, redirect



def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass

    return wrapper


@superuser_required()
class NearbyLocationFilterBackend(filters.DatatablesFilterBackend):

    def filter_queryset(self, request, queryset, view):
        nearby_pk = request.query_params.get('nearby_pk', None)
        if nearby_pk is not None:
            point = models.Request.objects.get(pk=nearby_pk).location
            return queryset.filter(location__distance_lt=(point, Distance(km=10))).order_by('pk')
        return queryset


@staff_member_required
def approve_request(request):
    try:
        pk = request.GET.get('pk')
        req = models.Request.objects.get(pk=pk)
    except models.Request.DoesNotExist as e:
        return JsonResponse({'error': e})

    req.status_completed = True
    req.save()
    return JsonResponse({'approved': 'True'})


@superuser_required()
class RequestViewSet(viewsets.ModelViewSet):
    queryset = models.Request.objects.all()
    serializer_class = serializers.RequestSerializer
    filter_backends = [NearbyLocationFilterBackend]
    renderer_classes = [DatatablesRenderer]


@superuser_required()
class RequestList(ListView):
    model = models.Request

def sort_on_urgency(request):
	request_list = models.Request.objects.annotate(u_count=Count('urgency_rating')).order_by('-u_count')
	return render(request, 'admin_panel/request_list.html', {'request_list': request_list})
