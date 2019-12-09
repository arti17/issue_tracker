from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.models import Issue, Project
from api.serializers import IssueSerializer, ProjectSerializer


def requests_view(request, *args, **kwargs):
    return render(request, 'scripts.html')


class LogoutView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
