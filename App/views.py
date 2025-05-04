from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import action

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the profile of the currently authenticated user
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='me')
    def get_user_profile(self, request):
        # Return the profile of the authenticated user as a single object
        user_profile = self.get_queryset().first()
        if user_profile:
            serializer = self.get_serializer(user_profile)
            return Response(serializer.data)
        return Response({'error': 'User profile not found'}, status=404)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        bio = request.data.get('bio')
        profile_picture = request.FILES.get('profile_picture')  # Handle profile picture upload

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, name=name, bio=bio, profile_picture=profile_picture)
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
