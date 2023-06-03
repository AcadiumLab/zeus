from rest_framework import generics

from tenant.serializers import OrganizationUserSerializer, OrganizationProfileSerializer
from utils import permissions


class CreateOrganizationUser(generics.CreateAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = (permissions.AllowAny,)


class CreateOrganizationUserProfile(generics.CreateAPIView):
    serializer_class = OrganizationProfileSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsVerified)
