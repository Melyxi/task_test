from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from task.models import Tasks, MyUserModel
from task.serializers import TaskSerializer, UserSerializer


class TaskView(ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        users = [item.pk for item in instance.users.all()]
        if request.user.pk in users:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({"error": "Нет доступа"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        users = [item.pk for item in instance.users.all()]
        if request.user.pk in users:
            self.perform_destroy(instance)
            return Response({"success": "Успешное удаление"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Нет доступа"})


class UserView(ModelViewSet):
    queryset = MyUserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

class AuthView(CreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = MyUserModel.objects.all()
    serializer_class = UserSerializer


class TasksUser(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, **kwargs):
        if kwargs['user_id'] == request.user.id:
            data = Tasks.objects.filter(users__in=[kwargs['user_id']])
            results = self.paginate_queryset(data, request, view=self)
            tasks = TaskSerializer(results, many=True)
            return self.get_paginated_response(tasks.data)
        else:
            return Response({'error': "Доступ запрещен"}, status=403)
