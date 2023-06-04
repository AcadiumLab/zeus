from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.db.models.signals import post_save
from django.dispatch import receiver

from tenant.models.user_model import OrganizationUser, OrganizationProfile
from utils.email import send_email


@receiver(post_save, sender=OrganizationUser)
def create_verification_code(sender, instance, created, **kwargs):
    if created:
        # Perform actions when a new User is created
        # For example, create a user profile
        OrganizationProfile.objects.create(
            organization=instance
        )

        token = default_token_generator.make_token(instance)

        activation_link = f'{settings.ACTIVATION_LINK_URL}?user_id={instance.id}&confirmation_token={token}'

        send_email(
            template_name='email/email_verification_message.html',
            receiver=['johnalbert.balansag@gmail.com'],
            subject='verification',
            data={'link': activation_link}
        )
