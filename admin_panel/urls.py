from django.urls import path, re_path, include
from . import views
from rest_framework import routers

app_name = 'admin_panel'

router = routers.DefaultRouter()
router.register(r'requests', views.RequestViewSet)

filter_requests = views.RequestViewSet.as_view(
    {
        'get': 'filter_requests',
    }
)

urlpatterns = [
    re_path('^api/', include(router.urls)),
    re_path('^api/nearby_requests/<int:pk>', views.FilterRequestViewSet.as_view({'get': 'list'})),
    path('requests/', views.RequestList.as_view(), name='requests'),
    path('approve_request/', views.approve_request, name='approve-request'),
    path('change_delta/', views.change_delta, name='volunteer-delta'),
    path('nearby/', views.NearbyForm.as_view(), name='nearby'),
]
