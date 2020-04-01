from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('postForm', views.postForm, name='postForm'),
]
