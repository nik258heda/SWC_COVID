from django.urls import path, re_path, include
from . import views
from rest_framework import routers

app_name = 'admin_panel'

router = routers.DefaultRouter()
router.register(r'requests', views.RequestViewSet)

urlpatterns = [
    re_path('^api/', include(router.urls)),
    path('requests/', views.RequestList.as_view(), name='requests'),
    path('approve_request/', views.approve_request, name='approve-request'),
    
]
