from django.urls import path, include
from . import views


app_name = 'admin_panel'

urlpatterns = [
    path('requests/', views.RequestList.as_view(), name='requests'),
    path('approve_request/', views.approve_request, name='approve-request'),
    path('surgency/', views.sort_on_urgency, name='surgency'),
    
]
