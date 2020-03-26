from django.views.generic import ListView
from . import models


class RequestList(ListView):
    model = models.Request
