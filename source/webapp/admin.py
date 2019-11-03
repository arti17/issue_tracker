from django.contrib import admin
from .models import Issue, Status, Type, Project, Team


class IssueAdmin(admin.ModelAdmin):
    list_display = ['summary', 'status', 'type', 'create_date']
    list_filter = ['status', 'type']
    search_fields = ['summary']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'start_date', 'end_date']
    list_filter = ['project', 'user']
    search_fields = ['project', 'user']


admin.site.register(Issue, IssueAdmin)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Project)
admin.site.register(Team, TeamAdmin)
