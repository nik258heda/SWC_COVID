from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('post_form', views.postForm, name='postForm'),
    path('main_page', views.mainPage, name="main_page"),
    path('open_post/<post_requestor_name>_<post_timestamp>', views.openPost, name="open_post"),

]
