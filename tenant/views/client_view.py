from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle

from tenant.models import Client
from tenant.serializers.client_serializer import ClientCreateSerializer, ClientSerializer, ClientUserSerializer
from utils import permissions


class CreateOrganizationDatabaseView(generics.CreateAPIView):
    serializer_class = ClientCreateSerializer
    # TODO ADD PERMISSION FOR TRIAL AND PAID USERS
    permission_classes = (permissions.IsAuthenticated, permissions.IsVerified, permissions.IsMainUser,)
    throttle_classes = [UserRateThrottle]


class ListOrganizationDatabaseView(generics.ListAPIView):
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsVerified,)
    queryset = Client.objects.all()

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


class CreateClientUser(generics.CreateAPIView):
    serializer_class = ClientUserSerializer
    # TODO ADD PERMISSION THAT CAN CHANGE TENANT
    permission_classes = (permissions.IsAuthenticated, permissions.IsVerified, permissions.IsMainUser,)
