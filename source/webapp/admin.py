from django.contrib import admin
from .models import Issue, Status, Type


class IssueAdmin(admin.ModelAdmin):
    list_display = ['summary', 'status', 'type', 'create_date']
    list_filter = ['status', 'type']
    search_fields = ['summary']


admin.site.register(Issue, IssueAdmin)
admin.site.register(Status)
admin.site.register(Type)
