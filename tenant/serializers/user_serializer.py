from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from tenant.serializers.client_serializer import ClientSerializer
from tenant.models import OrganizationProfile, OrganizationUser


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

    def create(self, validated_data):
        organization = self.context['request'].user
        profile = OrganizationProfile.objects.create_organization_profile(organization=organization, **validated_data)
        return profile
