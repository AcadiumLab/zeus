from django.urls import reverse
from django.test import RequestFactory

from django_tenants.utils import get_public_schema_name, get_tenant_model
from hypothesis.extra import django
from rest_framework import status
from tenant_users.tenants.utils import create_public_tenant
from django_tenants.test.client import TenantClient

from tenant.models import OrganizationProfile, OrganizationUser, SchoolType, SchoolLevel
from tenant.serializers import OrganizationProfileSerializer

TenantModel = get_tenant_model()


class OrganizationProfileSerializerTestCase(django.TestCase):

    def setUp(self):
        super().setUp()
        create_public_tenant(domain_url="my.test.domain", owner_email="admin@test.com", is_main=True)
        public_schema_name = get_public_schema_name()
        self.c = TenantClient(TenantModel.objects.filter(schema_name=public_schema_name).first())

    def test_profile_creation(self):
        user = OrganizationUser.objects.create(email='existing@example.com', password='existingpassword', is_main=True)

        self.valid_data = {
            'school_name': 'Example School',
            'street_address': '123 Main St',
            'postal_code': '10000',
            'state': 'CA',
            'city': 'Los Angeles',
            'country': 'US',
            'billing_same_as_address': True,
            'phone_number': '+6132000',
            'contact_person_name': 'My School head',
            'contact_person_email': 'head@school.com',
            'contact_person_phone': '+6312239',
            'school_type': SchoolType.objects.create(name='Private').id,
            'school_level': SchoolLevel.objects.create(name='Elementary').id,
            'enrollment_capacity': 1000,
        }
        factory = RequestFactory()
        request = factory.post(reverse('tenant:organization-profile-create'))
        request.user = user
        serializer = OrganizationProfileSerializer(data=self.valid_data, context={
            'request': request
        })
        self.assertTrue(serializer.is_valid(raise_exception=True))
        profile = serializer.save()
        self.assertIsInstance(profile, OrganizationProfile)
        self.assertEqual(profile.organization, user)

        # Verify that the profile is saved in the database
        profile_from_db = OrganizationProfile.objects.get(pk=profile.pk)
        self.assertEqual(profile_from_db, profile)

    def test_create_invalid_organization_profile(self):
        invalid_data = {
            'street_address': 2,
        }

        user = OrganizationUser.objects.create(email='existing@example.com', is_main=True)
        user.set_password('existingpassword')
        user.save()
        self.c.login(
            username='existing@example.com',
            password='existingpassword'
        )

        serializer = OrganizationProfileSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

        response = self.c.post(reverse('tenant:organization-profile-create'), invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
