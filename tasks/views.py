from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer,SignupSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser






@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TaskListCreateView(APIView):
    def get(self, request):

        if request.user.is_staff:
            tasks = Task.objects.all()
        
        else:
            tasks = Task.objects.filter(user=request.user)
        
        status_filter = request.query_params.get('status')
        
        if status_filter == "completed":
            tasks = tasks.filter(is_completed=True)
        elif status_filter == "pending":
            tasks = tasks.filter(is_completed=False)

        search = request.query_params.get('search')
        if search:
            tasks = tasks.filter(title__icontains=search)

        pagination = PageNumberPagination()
        pagination.page_size=3
        paginated_tasks=pagination.paginate_queryset(tasks, request)

        serializer = TaskSerializer(paginated_tasks, many=True)
        return pagination.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TaskDetailView(APIView):
    def get_obj(self, id, user):
        try:
            if user.is_staff:
                return Task.objects.get(id=id)
            return Task.objects.get(id=id, user=user)
        except Task.DoesNotExist:
            return None
        
    def get(self, request, id):
        task = self.get_obj(id, user=request.user)
        if not task:
            return Response({'error':'task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, id):
        task = self.get_obj(id, user=request.user)
        if not task:
            return Response({'error':'task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        task = self.get_obj(id, user=request.user)
        if not task:
            return Response({'error':'task not found'}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        if User.objects.filter(username=serializer.validated_data['username']).exists():
            return Response({'error':'user already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User(username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'])
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({'message':'user created sucssefully'})
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
    except:
        pass
    return Response({'message': 'Logged out successfully'})


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_account_view(request):
    try:
        request.user.auth_token.delete()
    except:
        pass
    request.user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
