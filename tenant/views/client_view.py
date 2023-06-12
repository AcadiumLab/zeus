from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle

from tenant.models import Client, OrganizationUser, Domain
from tenant.serializers.client_serializer import ClientCreateSerializer, ClientSerializer, ClientDomainCreateSerializer, \
    ClientUserProfileSerializer
from utils import permissions


class OrganizationDatabaseView(generics.ListCreateAPIView):
    serializer_class = {
        'get': ClientSerializer,
        'post': ClientCreateSerializer,
    }
    # TODO ADD PERMISSION FOR TRIAL AND PAID USERS
    permission_classes = (permissions.IsAuthenticated, permissions.IsVerified, permissions.IsMainUserOrReadOnly,)
    queryset = Client.objects.all()
    throttle_classes = [UserRateThrottle]

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """

        assert self.serializer_class.get(self.request.method.lower(), None) is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.serializer_class[self.request.method.lower()]

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.request.user.tenants.all().exclude(schema_name='public')
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset


class CreateClientUser(generics.ListCreateAPIView):
    serializer_class = ClientUserProfileSerializer
    queryset = OrganizationUser.objects.all()
    # TODO ADD PERMISSION THAT CAN CHANGE TENANT
    permission_classes = (permissions.IsAuthenticated, permissions.IsVerified, permissions.IsMainUserOrReadOnly,)


class CreateClientDomain(generics.ListCreateAPIView):
    serializer_class = ClientDomainCreateSerializer
    queryset = Domain.objects.all()
    # TODO ADD PERMISSION THAT CAN CHANGE TENANT
    permission_classes = (permissions.IsAuthenticated, permissions.IsVerified, permissions.IsMainUserOrReadOnly,)
