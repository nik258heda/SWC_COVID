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
from django.views.generic import FormView
from django.db.models import Count
from django.shortcuts import render
from . import forms
from django.contrib.gis.geos import Point, GEOSGeometry


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
class FilterRequestViewSet(viewsets.ModelViewSet):
    queryset = models.Request.objects.all()
    serializers = serializers.RequestSerializer

    def get_request(self, pk):
        queryset = self.queryset
        point = models.Request.objects.get(pk=pk).location
        return queryset.filter(location__distance_lt=(point, Distance(km=10))).order_by('pk')

    def list(self, request, *args, **kwargs):
        pk = 1
        queryset = self.get_request(pk)


@superuser_required()
class RequestViewSet(viewsets.ModelViewSet):
    queryset = models.Request.objects.all()
    serializer_class = serializers.RequestSerializer
    filter_backends = [NearbyLocationFilterBackend]
    renderer_classes = [DatatablesRenderer]


@superuser_required()
class RequestList(ListView):
    model = models.Request

    
@staff_member_required
def change_delta(request):
    # if request.method == 'POST':
    try:
        pk = request.GET.get('pk')
        delta = int(request.GET.get('delta'))
        req = models.Request.objects.get(pk=pk)
    except models.Request.DoesNotExist as e:
        return JsonResponse({'error': e})

    req.v_const += delta
    req.save()
    return JsonResponse({'approved': 'True'})



class NearbyForm(FormView):
    template_name = 'admin_panel/nearby.html'
    form_class = forms.RequestForm
    success_url = ''

    def post(self, request, *args, **kwargs):
        form_class = self.form_class
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            print('invalid')
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context=context)

    def form_valid(self, form, **kwargs):
        point = form.cleaned_data['location']
        point = GEOSGeometry(point)
        radius = form.cleaned_data['radius']
        print(point, radius)
        queryset = models.Request.objects.filter(location__distance_lte=(point, Distance(km=radius)))
        queryset=queryset.order_by('urgency_rating')
        context = self.get_context_data(**kwargs)
        context['requests'] = queryset
        return self.render_to_response(context)

