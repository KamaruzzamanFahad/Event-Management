from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.tokens import default_token_generator 
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def send_email(sender, instance, created, **kwargs):
    if created:
        tocken = default_token_generator.make_token(instance)
        activations_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{tocken}"

        subject = "Activate Your Account"
        message = f"Hi {instance.username} Please active your account by clicking this link bellow {activations_url} Thank You"
        recipient_list =[instance.email]

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"Faild to send email to: {instance.email} : {str(e)}")