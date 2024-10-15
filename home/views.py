from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import Todo
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):

    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer
    def list(self, request, *args, **kwargs):

        """
        this request will show the all of user todos

        """


        queryset = self.request.user.todos
        if queryset.exists():
            serializer = TodoSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'this user todos not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):

        """
        this request will create a new todo for user
        """

        serializer = TodoSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response({"message": "Todo added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):

        """this request will update an existing todo"""

        queryset = get_object_or_404(Todo, pk=kwargs['pk'])
        serializer = TodoSerializer(data=request.POST, instance=queryset, partial=True)
        if serializer.is_valid():
            if request.user == queryset.user:
                serializer.save()
                return Response({"message": "your to do updated successfully"}, status=status.HTTP_200_OK)
            return Response({"you cant edit another users todo"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):

        """this request will delete an existing todo of logged in user"""

        queryset = get_object_or_404(Todo, pk=kwargs['pk'])
        if request.user == queryset.user:
            queryset.delete()
            return Response({"message": "your to do deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"you dont have permission to delete this todo"}, status=status.HTTP_400_BAD_REQUEST)


