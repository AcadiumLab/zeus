from django.contrib.auth import get_user_model
from django.urls import reverse
from django_tenants.utils import get_tenant_model, get_public_schema_name
from hypothesis import given, settings
from hypothesis.extra import django
from rest_framework import status
from tenant_users.tenants.utils import create_public_tenant

from tenant.models import OrganizationUser
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient

from tenant.serializers import OrganizationUserSerializer

TenantUser = get_user_model()
TenantModel = get_tenant_model()


class OrganizationUserTestCase(django.TestCase):
    """This is a property-based test that ensures model correctness."""

    @given(django.from_model(OrganizationUser))
    @settings(deadline=None)
    def test_model_properties(self, instance: TenantUser) -> None:
        """Tests that instance can be saved and has correct representation."""
        instance.save()

        assert instance.has_verified_email() == instance.is_verified

        # Test UserProfile.get_full_name()
        assert instance.get_full_name() == str(instance)

        # Test UserProfile.get_short_name()
        assert instance.get_short_name() == instance.email


class OrganizationUserSerializerTestCase(django.TestCase):

    def setUp(self):
        super().setUp()
        create_public_tenant(domain_url="my.test.domain", owner_email="admin@test.com", is_main=True)
        public_schema_name = get_public_schema_name()
        self.c = TenantClient(TenantModel.objects.filter(schema_name=public_schema_name).first())

    def test_create_user(self):
        data = {
            'password': 'testpassword',
            'email': 'test@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_main': True,
        }

        serializer = OrganizationUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertIsInstance(user, OrganizationUser)
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('testpassword'))
        # Assert other attributes of the created user

        # Verify that the user is saved in the database
        user_from_db = OrganizationUser.objects.get(pk=user.pk)
        self.assertEqual(user_from_db, user)

    def test_create_existing_user(self):
        OrganizationUser.objects.create(email='existing@example.com', password='existingpassword', is_main=True)

        data = {
            'password': 'newpassword',
            'email': 'existing@example.com',
            'first_name': 'Existing',
            'last_name': 'User',
            'is_main': True,
        }

        serializer = OrganizationUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        response = self.c.post(reverse('tenant:organization-user-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
