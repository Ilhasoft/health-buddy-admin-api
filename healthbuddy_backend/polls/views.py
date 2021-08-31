from django.shortcuts import render
from rest_framework import viewsets
from .models import Polls
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from .serializers import PollSerializer


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = Polls.objects.all()
    filterset_fields = ["id", "author", "name", "link", "is_active"]
    search_fields = ["name", "author", "link", "is_active"]
    ordering_fields = ["name", "author", "link", "is_active"]
    http_method_names = ["get", "put", "post", "delete"]


    @action(methods=["put"], detail=True, permission_classes=[IsAdminUser])
    def active(self, request, pk=None):
        poll = self.get_object()
        poll.is_active = True
        poll.save()

        return Response(data={"message": f"{poll.name} has been activated!"}, status=200)

    @action(methods=["POST"], detail=True, permission_classes=[IsAdminUser])
    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(author=user.username)