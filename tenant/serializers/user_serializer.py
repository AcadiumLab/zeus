from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from tenant.models import OrganizationProfile, OrganizationUser
from tenant.serializers.client_serializer import ClientSerializer


class OrganizationUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_main = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    tenants = serializers.ManyRelatedField(read_only=True, child_relation=ClientSerializer(),
                                           source='user_set',
                                           )

    class Meta:
        model = OrganizationUser
        exclude = ()

    def create(self, validated_data):
        user = OrganizationUser.objects.create_user(
            **validated_data,
            is_main=True
        )

        return user

    def update(self, instance, validated_data):
        validated_data.pop('password')
        return super().update(instance, validated_data)

    def validate_email(self, value):
        if OrganizationUser.objects.filter(email=value).exists():
            raise ValidationError('Email address already exists.')
        return value


class OrganizationProfileSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrganizationProfile
        exclude = ()
        extra_kwargs = {
            'school_name': {'required': True},
            'street_address': {'required': True},
            'postal_code': {'required': True},
            'state': {'required': True},
            'city': {'required': True},
            'country': {'required': True},
            'phone_number': {'required': True},
            'contact_person_name': {'required': True},
            'contact_person_email': {'required': True},
            'contact_person_phone': {'required': True},
        }


class AuthenticateOrganizationSerializer(Serializer):
    username = serializers.EmailField(write_only=True, read_only=False)
    password = serializers.CharField(write_only=True, read_only=False)
    grant_type = serializers.CharField(write_only=True, read_only=False)

    access_token = serializers.CharField(read_only=True)
    token_type = serializers.CharField(read_only=True)
    scope = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    expires_in = serializers.IntegerField(read_only=True)
