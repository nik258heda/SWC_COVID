from django.views.generic import ListView
from . import models
from django.http import JsonResponse


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
