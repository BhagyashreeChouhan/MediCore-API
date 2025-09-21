from rest_framework.response import Response
from rest_framework import generics, status
from utils.permissions import role_permission
from .models import Patient
from rest_framework.viewsets import ModelViewSet
from .serializers import PatientSerializer

# Create your views here.
class PatientViewset(ModelViewSet):
    permission_classes = [role_permission(["ADMIN", "RECEPTIONIST", "DOCTOR", "NURSE"])]
    queryset = Patient.active.all()
    serializer_class = PatientSerializer
    lookup_field = "uuid"

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [role_permission(["ADMIN", "RECEPTIONIST"])()]
        elif self.action in ["list", "retrieve"]:
            return [role_permission(["ADMIN", "RECEPTIONIST", "DOCTOR", "NURSE"])()]
        elif self.action == "destroy":
            return [role_permission(["ADMIN"])()]
        return [role_permission([])()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.soft_delete(deleted_by=self.request.user)