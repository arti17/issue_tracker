from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.register_view, name='register'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/update/', views.UserPersonalInfoChangeView.as_view(), name='user_update_info'),
    path('user/<int:pk>/password_change/', views.UserPasswordChangeView.as_view(), name='user_change_password'),
]
