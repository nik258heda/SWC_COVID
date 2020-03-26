from django.urls import path, include
from . import views


app_name = 'admin_panel'

urlpatterns = [
    path('requests/', views.RequestList.as_view(), name='requests'),
]
