from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.views import TokenView
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from tenant.models import OrganizationUser
from tenant.serializers import OrganizationUserSerializer, OrganizationProfileSerializer, \
    AuthenticateOrganizationSerializer
from utils import permissions
from utils.throttling import AccountActivationThrottle


class CreateOrganizationUser(generics.CreateAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = (permissions.AllowAny,)


class CreateOrganizationUserProfile(generics.CreateAPIView):
    serializer_class = OrganizationProfileSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsVerified)
    throttle_classes = [UserRateThrottle]


class UserActivationView(generics.RetrieveAPIView):
    queryset = OrganizationUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = OrganizationUserSerializer
    throttle_classes = [AccountActivationThrottle]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description='User ID', type=openapi.TYPE_INTEGER),
            openapi.Parameter('confirmation_token', openapi.IN_QUERY, description='Confirmation Token',
                              type=openapi.TYPE_STRING),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', '')
        confirmation_token = request.query_params.get('confirmation_token', '')

        user = get_object_or_404(self.get_queryset(), pk=user_id)

        if not default_token_generator.check_token(user, confirmation_token):
            return Response({'msg': 'Token is invalid or expired. Please request another confirmation email by '
                                    'signing in.'}
                            , status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active and not user.is_verified:
            user.is_active = True
            user.is_verified = True
            user.save()

        serializer = self.get_serializer(user)
        return Response(serializer.data)


class OrganizationAuthenticationView(generics.CreateAPIView):
    serializer_class = AuthenticateOrganizationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        view = TokenView()
        new_request = HttpRequest()
        new_request.method = 'POST'

        new_request.POST['username'] = request.data.get('email', request.data['username'])
        new_request.POST['password'] = request.data['password']
        new_request.POST['grant_type'] = 'password'
        new_request.POST['client_id'] = settings.CLIENT_ID
        new_request.POST['client_secret'] = settings.CLIENT_SECRET
        response = view.post(new_request)

        return response
