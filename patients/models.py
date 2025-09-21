from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone
from django.core.validators import RegexValidator

# Create your models here.
def generate_mrn():
    today = timezone.now().strftime("%Y%m%d")
    return f"MRN{today}{uuid.uuid4().hex[:6].upper()}"

class ActivePatientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Patient(models.Model):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    mrn = models.CharField(default=generate_mrn ,max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15, validators=[
            RegexValidator(
                r'^\+?\d{10,15}$',
                "Enter a valid phone number with country code (10–15 digits)."
            )
        ],)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, validators=[
            RegexValidator(
                r'^\+?\d{10,15}$',
                "Enter a valid phone number with country code (10–15 digits)."
            )
        ], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients_created')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients_updated')
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients_deleted')

    objects = models.Manager()
    active = ActivePatientManager()
    
    def soft_delete(self, deleted_by=None):
        self.is_active = False
        self.deleted_at = timezone.now()
        if deleted_by:
            self.deleted_by = deleted_by
        self.save()

    def __str__(self):
        return f"{self.mrn}: {self.first_name} {self.last_name}"