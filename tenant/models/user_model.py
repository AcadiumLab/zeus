from django.conf import settings
from django.db import models, connection
from django.utils.translation import gettext_lazy as _
from django_tenants.utils import get_public_schema_name
from tenant_users.tenants.models import UserProfile, SchemaError

from tenant.models import SchoolType, SchoolLevel


class OrganizationProfileManager(models.Manager):
    def create_organization_profile(self, organization, school_name, street_address,
                                    postal_code, state, city, country, street_address_extra=None,
                                    billing_same_as_address=False,
                                    billing_street_address=None, billing_street_address_extra=None,
                                    billing_postal_code=None, billing_state=None, billing_city=None,
                                    billing_country=None, phone_number=None, telephone_number=None,
                                    website=None, contact_person_name=None, contact_person_email=None,
                                    contact_person_phone=None, school_type=None, school_level=None,
                                    enrollment_capacity=1):

        if connection.schema_name != get_public_schema_name():
            raise SchemaError(
                'Schema must be public for UserProfileManager user creation',
            )

        organization_profile = self.model(
            organization=organization,
            school_name=school_name,
            street_address=street_address,
            street_address_extra=street_address_extra,
            postal_code=postal_code,
            state=state,
            city=city,
            country=country,
            billing_same_as_address=billing_same_as_address,
            billing_street_address=billing_street_address,
            billing_street_address_extra=billing_street_address_extra,
            billing_postal_code=billing_postal_code,
            billing_state=billing_state,
            billing_city=billing_city,
            billing_country=billing_country,
            phone_number=phone_number,
            telephone_number=telephone_number,
            website=website,
            contact_person_name=contact_person_name,
            contact_person_email=contact_person_email,
            contact_person_phone=contact_person_phone,
            school_type=school_type,
            school_level=school_level,
            enrollment_capacity=enrollment_capacity
        )
        organization_profile.save()
        return organization_profile


class OrganizationUser(UserProfile):
    is_main = models.BooleanField(_('User main account'), default=False)


class OrganizationProfile(models.Model):
    organization = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    # Additional fields for school organization
    school_name = models.CharField(max_length=255, null=True)

    # Address
    street_address = models.CharField(max_length=255, null=True)
    street_address_extra = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)

    # Billing Address
    billing_street_address = models.CharField(max_length=255, blank=True, null=True)
    billing_street_address_extra = models.CharField(max_length=255, blank=True, null=True)
    billing_postal_code = models.CharField(max_length=255, blank=True, null=True)
    billing_state = models.CharField(max_length=255, blank=True, null=True)
    billing_city = models.CharField(max_length=255, blank=True, null=True)
    billing_country = models.CharField(max_length=255, blank=True, null=True)

    # Flags for checking billing address
    billing_same_as_address = models.BooleanField(default=False)

    # Additional Information
    phone_number = models.CharField(max_length=20, null=True)
    telephone_number = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # Contact Person fields
    contact_person_name = models.CharField(max_length=255, null=True)
    contact_person_email = models.EmailField(null=True)
    contact_person_phone = models.CharField(max_length=20, null=True)

    # Extra Info
    school_type = models.ForeignKey(SchoolType, on_delete=models.PROTECT, null=True)
    school_level = models.ForeignKey(SchoolLevel, on_delete=models.PROTECT, null=True)
    enrollment_capacity = models.PositiveIntegerField(default=1)
    # ... add more fields as needed

    objects = OrganizationProfileManager()
