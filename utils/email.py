from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email(
        template_name: str = None,
        receiver: list = None,
        subject: str = "",
        body: str = None,
        data: dict = dict
):
    """Send Email"""

    email = EmailMessage()
    email.body = body

    if template_name and not body:
        email.body = render_to_string(template_name, data)
        email.content_subtype = 'html'

    email.subject = subject
    email.to = receiver

    email.send(fail_silently=False)
