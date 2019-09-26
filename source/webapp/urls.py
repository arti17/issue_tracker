from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('issue/<int:pk>', views.IssueView.as_view(), name='detail'),
    path('create_issue/', views.IssueCreateView.as_view(), name='create_issue'),
    path('update_issue/<int:pk>', views.IssueUpdateView.as_view(), name='update_issue'),
    path('delete_issue/<int:pk>', views.IssueDeleteView.as_view(), name='delete_issue'),
]
