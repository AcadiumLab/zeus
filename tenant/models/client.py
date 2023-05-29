from django.utils import timezone

from django.db import models
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase


def default_date():
    return timezone.now() + timezone.timedelta(days=30)


class Client(TenantBase):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(default=default_date)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)


class Domain(DomainMixin):
    pass
