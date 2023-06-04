from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tenant_users.tenants.models import ExistsError
from tenant_users.tenants.tasks import provision_tenant

from tenant.models import Client


class ClientSerializer(serializers.ModelSerializer):
    detail = serializers.CharField(read_only=True)
    success = serializers.BooleanField(read_only=True)

    class Meta:
        model = Client
        fields = ('name', 'slug', 'detail', 'success',)
        extra_kwargs = {
            'name': {'write_only': True},
            'slug': {'write_only': True}
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
