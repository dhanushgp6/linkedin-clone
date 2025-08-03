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
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        # Debug: Print current user info
        print(f"🔍 Request user: {self.request.user}")
        print(f"🔍 Is authenticated: {self.request.user.is_authenticated}")
        print(f"🔍 Username: {getattr(self.request.user, 'username', 'AnonymousUser')}")
        
        if self.request.user.is_authenticated:
            print(f"✅ Creating post for authenticated user: {self.request.user.username}")
            serializer.save(author=self.request.user)
        else:
            print("❌ User not authenticated, checking session...")
            
            # Try to get user from session data
            user_id = self.request.session.get('_auth_user_id')
            if user_id:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    user = User.objects.get(id=user_id)
                    print(f"✅ Found user from session: {user.username}")
                    serializer.save(author=user)
                    return
                except User.DoesNotExist:
                    print("❌ User from session not found")
            
            # If still no user, return error instead of using fallback
            from rest_framework.exceptions import AuthenticationFailed
            raise AuthenticationFailed("You must be logged in to create posts")

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]  # Change this line
    
    def perform_create(self, serializer):
        # Get the user from the session or use a default user
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            # For debugging, create posts with first available user
            from django.contrib.auth import get_user_model
            User = get_user_model()
            first_user = User.objects.first()
            if first_user:
                serializer.save(author=first_user)
            else:
                # Create a default user if none exists
                default_user = User.objects.create_user(
                    username='demo_user',
                    email='demo@example.com',
                    password='demo123'
                )
                serializer.save(author=default_user)

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
