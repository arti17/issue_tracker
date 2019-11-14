from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('issue/<int:pk>', views.IssueView.as_view(), name='issue_detail'),
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
    path('projects/', views.ProjectView.as_view(), name='projects_list'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/create', views.ProjectCreateView.as_view(), name='create_project'),
    path('project/delete/<int:pk>', views.ProjectDeleteView.as_view(), name='delete_project'),
    path('project/update/<int:pk>', views.ProjectUpdateView.as_view(), name='update_project'),
    path('project/add-issue/<int:pk>', views.ProjectCreateIssueView.as_view(), name='create_project_issue'),
    path('project/add-users/<int:pk>', views.AddProjectUsers.as_view(), name='add_project_users'),
]
