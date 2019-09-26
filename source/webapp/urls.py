from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('issue/<int:pk>', views.IssueView.as_view(), name='detail'),
    path('issue/create/', views.IssueCreateView.as_view(), name='create_issue'),
    path('issue/update/<int:pk>', views.IssueUpdateView.as_view(), name='update_issue'),
    path('issue/delete/<int:pk>', views.IssueDeleteView.as_view(), name='delete_issue'),
    path('statuses/', views.StatusView.as_view(), name='statuses_list'),
    path('types/', views.TypeView.as_view(), name='types_list'),
    path('status/delete/<int:pk>', views.StatusDeleteView.as_view(), name='delete_status'),
    path('type/delete/<int:pk>', views.TypeDeleteView.as_view(), name='delete_type'),
    path('status/create/', views.StatusCreateView.as_view(), name='create_status'),
    path('type/create/', views.TypeCreateView.as_view(), name='create_type'),
    path('status/update/<int:pk>', views.StatusUpdateView.as_view(), name='update_status'),
    path('type/update/<int:pk>', views.TypeUpdateView.as_view(), name='update_type'),
]
