import random
import string
import secrets
from django.core.mail import send_mail
from smtplib import SMTPException
from socket import error as SocketError
from django.conf import settings

def random_generated_password(length=10):
    selection_list = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(selection_list) for _ in range(length))

def sendRegistrationEmail(username, role, email, password):
    try:
        send_mail(
            subject="Welcome to Hospital Management System",
            message=f"""
            Hello {username},

            Your account has been created successfully.

            Role: {role}
            Username: {email}
            Temporary Password: {password}

            Please login and reset your password using the "Reset Password" option.

            Login here: http://127.0.0.1:8000/users/login/
                    """,

            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            
        )
        
        return True
    except SMTPException as e:
        return f"SMTP error occurred: {str(e)}"
    except SocketError as e:
        return f"Network error occurred while sending email: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"