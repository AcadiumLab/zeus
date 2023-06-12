from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tenant_users.tenants.models import ExistsError
from tenant_users.tenants.tasks import provision_tenant

from tenant.models import Client, OrganizationUser, Domain
from tenant.models.client_model import Department, Role
from tenant.models.user_model import OrganizationUserProfile


class ClientCreateSerializer(serializers.ModelSerializer):
    detail = serializers.CharField(read_only=True)
    success = serializers.BooleanField(read_only=True)

    class Meta:
        model = Client
        fields = ('name', 'slug', 'on_trial', 'paid_until', 'detail', 'success',)
        extra_kwargs = {
            'name': {'write_only': True},
            'slug': {'write_only': True},
            'paid_until': {'read_only': True},
            'on_trial': {'read_only': True},
        }

    def create(self, validated_data):
        try:
            provision_tenant(
                tenant_name=validated_data['name'],
                tenant_slug=validated_data['slug'],
                user_email=self.context['request'].user.email
            )
        except ExistsError as err:
            raise ValidationError({
                'detail': err.__str__(),
                'success': False
            })

        return {
            'detail': 'Creating database for %s, this process may take time please wait.' % validated_data['name'],
            'success': True
        }


class ClientDomainCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        exclude = ()


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ()


class ClientUserSerializer(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), write_only=True)

    class Meta:
        model = OrganizationUser
        exclude = ('password', 'tenants',)
        extra_kwargs = {
            'is_main': {'read_only': True},
            'is_verified': {'read_only': True},
            'is_active': {'read_only': True},
            'last_login': {'read_only': True},
        }


class ClientUserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(write_only=True, required=True, allow_blank=False)
    is_active = serializers.BooleanField(read_only=True, source='organization.is_active')
    is_verified = serializers.BooleanField(read_only=True, source='organization.is_verified')
    is_main = serializers.BooleanField(read_only=True, source='organization.is_main')
    last_login = serializers.DateTimeField(read_only=True, source='organization.last_login')
    tenant = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Client.objects.all())

    class Meta:
        model = OrganizationUserProfile
        exclude = ('organization',)

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        tenant = validated_data.pop('tenant')

        profile = OrganizationUserProfile()
        for key, value in validated_data.items():
            setattr(profile, key, value)

        user = OrganizationUser.objects.create_user(
            email=email,
            password=password,
            is_main=False
        )

        setattr(profile, 'organization', user)

        profile.save()
        setattr(profile, 'email', email)

        tenant.add_user(
            user_obj=user
        )

        return profile


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ()
        extra_kwargs = {
            'projects': {'read_only': True},
        }


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        exclude = ()
        extra_kwargs = {
            'projects': {'read_only': True},
        }
