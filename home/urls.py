from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'home'

urlpatterns = [
    path('', views.pathwayToHome),
    path('home_page/<latitude>_<longitude>', views.home, name='home'),
    path('post_form/<latitude>_<longitude>', views.postForm, name='postForm'),
    path('main_page/<latitude>_<longitude>', views.mainPage, name="main_page"),
    path('open_post/<post_requestor_name>_<post_timestamp>_<latitude>_<longitude>', views.openPost, name="open_post"),
]
