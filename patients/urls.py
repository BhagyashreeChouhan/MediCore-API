from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PatientViewset

router = DefaultRouter()
router.register(r'', PatientViewset, basename='patients')

urlpatterns = router.urls