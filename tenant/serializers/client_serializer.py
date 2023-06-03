from rest_framework import serializers

from tenant.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ()
