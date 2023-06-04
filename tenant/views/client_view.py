from rest_framework import generics
from rest_framework.throttling import UserRateThrottle

from tenant.serializers.client_serializer import ClientSerializer
from utils import permissions


class CreateOrganizationDatabaseView(generics.CreateAPIView):
    serializer_class = ClientSerializer
    # TODO ADD PERMISSION FOR TRIAL AND PAID USERS
    permission_classes = (permissions.IsAuthenticated, permissions.IsVerified, permissions.IsMainUser,)
    throttle_classes = [UserRateThrottle]
