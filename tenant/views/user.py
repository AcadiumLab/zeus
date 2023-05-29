from rest_framework import generics, permissions

from tenant.serializers import OrganizationUserSerializer


class CreateOrganizationUser(generics.CreateAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = (permissions.AllowAny, )


class CreateOrganizationUserProfile(generics.CreateAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = (permissions.IsAuthenticated, )
