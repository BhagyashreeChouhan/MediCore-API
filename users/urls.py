from django.urls import path
from .views import UserProfileAPIView, LoginAPIView, RegisterAPIView, LogoutAPIView

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='user_profile'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('logout/', LogoutAPIView.as_view(), name="logout")
]