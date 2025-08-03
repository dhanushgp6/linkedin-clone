from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from .models import Post
from .serializers import PostSerializer, UserSerializer
import json

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]  # Allow anyone to read posts
        return [permissions.IsAuthenticated()]  # Require auth for creating posts
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@method_decorator(csrf_exempt, name='dispatch')
class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to view user posts
    
    def get_queryset(self):
        username = self.kwargs['username']
        return Post.objects.filter(author__username=username)

@api_view(['POST'])
@csrf_exempt
@permission_classes([permissions.AllowAny])
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    bio = request.data.get('bio', '')
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, email=email, password=password, bio=bio)
    login(request, user)
    
    # Return user data for frontend
    return Response({
        'message': 'User created successfully', 
        'username': username,
        'user_id': user.id
    })

@api_view(['POST'])
@csrf_exempt
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response({
            'message': 'Login successful', 
            'username': username,
            'user_id': user.id
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@csrf_exempt
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})

@api_view(['GET'])
@csrf_exempt
@permission_classes([permissions.AllowAny])
def user_profile_view(request, username):
    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@ensure_csrf_cookie
@permission_classes([permissions.AllowAny])
def csrf_token_view(request):
    return Response({'csrfToken': get_token(request)})
