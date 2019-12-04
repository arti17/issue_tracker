from webapp.models import Issue, Project
from rest_framework import serializers


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'summary', 'description', 'status', 'type', 'create_date', 'update_date', 'project', 'created_by', 'assigned_to')


class ProjectSerializer(serializers.ModelSerializer):
    issues = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'summary', 'description', 'create_date', 'update_date', 'status', 'issues')
