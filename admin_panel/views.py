from django.views.generic import ListView
from . import models
from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import render, redirect


def approve_request(request):
    try:
        pk = request.GET.get('pk')
        req = models.Request.objects.get(pk=pk)
    except models.Request.DoesNotExist as e:
        return JsonResponse({'error': e})

    req.status_completed = True
    req.save()
    return JsonResponse({'approved': 'True'})


class RequestList(ListView):
    model = models.Request

def sort_on_urgency(request):
	request_list = models.Request.objects.annotate(u_count=Count('urgency_rating')).order_by('-u_count')
	return render(request, 'admin_panel/request_list.html', {'request_list': request_list})
