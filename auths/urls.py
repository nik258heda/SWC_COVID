from django.urls import path, include
from . import views as auths_views
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings 
from django.contrib.auth import views as auth_views

app_name = 'auths'

urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
	path('register/', auths_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="auths/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="auths/logout.html"), name='logout'),
    path('addincol/', auths_views.profileCollectionView, name='profileCollection'),
]

