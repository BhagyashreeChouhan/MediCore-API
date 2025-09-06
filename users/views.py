from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer
from utils.permissions import role_permission
from utils.utils import sendRegistrationEmail, random_generated_password

# Create your views here.
class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user
    
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({
                "message":"Invalid credentials."
            },status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            "message":"Login successful.",
            "user":UserSerializer(user).data,
            "refresh_token":str(refresh),
            "access_token":str(refresh.access_token)}, status=status.HTTP_200_OK)
    
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [role_permission(["ADMIN"])]
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = random_generated_password()
        user = serializer.save(password=password)
        email_sent = sendRegistrationEmail(
            username=user.username,
            role=user.role,
            email=user.email,
            password=password)
        return Response({
             "message": "Account created & email sent." if email_sent == True else f"Account created but email failed: {email_sent}",
            "user": serializer.data
           }, status=status.HTTP_201_CREATED)
    
class LogoutAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            print(refresh_token)
            token = RefreshToken(refresh_token)
            print(token)
            token.blacklist()
            return Response({
                "message": "Logout successful."
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)