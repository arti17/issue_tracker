from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api import views


router = routers.DefaultRouter()
router.register(r'issues', views.IssueViewSet)
router.register(r'projects', views.ProjectViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_auth_token'),
    path('logout/', views.LogoutView.as_view(), name='delete_auth_token'),
    path('requests/', views.requests_view, name='requests'),
]
