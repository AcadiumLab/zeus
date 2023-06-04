from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.throttling import UserRateThrottle

from tenant.models import OrganizationProfile, OrganizationUser
from tenant.serializers import OrganizationUserSerializer, OrganizationProfileSerializer
from utils import permissions


class CreateOrganizationUser(generics.CreateAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = (permissions.AllowAny,)


class CreateOrganizationUserProfile(generics.UpdateAPIView):
    serializer_class = OrganizationProfileSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsVerified)
    throttle_classes = [UserRateThrottle]
    queryset = OrganizationProfile.objects.all()

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {'organization': self.request.user}
        print(filter_kwargs)
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class RetrieveOrganizationView(generics.RetrieveAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = OrganizationUser.objects.all()

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """

        return self.request.user


class RetrieveOrganizationProfile(generics.RetrieveAPIView):
    serializer_class = OrganizationProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = OrganizationProfile.objects.all()
    throttle_classes = [UserRateThrottle]

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {'organization': self.request.user}
        print(filter_kwargs)
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
