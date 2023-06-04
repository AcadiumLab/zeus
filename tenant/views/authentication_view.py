from django.conf import settings
from django.http import HttpRequest
from oauth2_provider.views import TokenView
from rest_framework import generics
from rest_framework.parsers import FormParser

from tenant.serializers import AuthenticateOrganizationSerializer
from utils import permissions


class OrganizationAuthenticationView(generics.CreateAPIView):
    serializer_class = AuthenticateOrganizationSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = (FormParser,)

    def create(self, request, *args, **kwargs):
        view = TokenView()
        new_request = HttpRequest()
        new_request.method = request.method
        new_request.content_type = request.content_type
        new_request.content_params = request.content_params
        for key, value in dict(request.POST).items():
            new_request.POST[key] = request.POST[key]

        new_request.POST['client_id'] = settings.CLIENT_ID
        new_request.POST['client_secret'] = settings.CLIENT_SECRET

        response = view.post(new_request)

        return response
