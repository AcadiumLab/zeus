from django.urls import path

from .views import CreateOrganizationUser, CreateOrganizationUserProfile, RetrieveOrganizationView, \
    RetrieveOrganizationProfile
from .views.activation_view import UserActivationView
from .views.authentication_view import OrganizationAuthenticationView
from .views.client_view import CreateClientUser, \
    CreateClientDomain, OrganizationDatabaseView

app_name = 'tenant'
urlpatterns = [
    path('organization-user/create/', CreateOrganizationUser.as_view(), name='organization-signup'),
    path('organization-profile/update/', CreateOrganizationUserProfile.as_view(), name='organization-profile-create'),
    path('organization-activate/', UserActivationView.as_view(), name='organization-user-activation'),

    path('organization-user/', RetrieveOrganizationView.as_view(), name='retrieve-organization'),
    path('organization-profile/', RetrieveOrganizationProfile.as_view(), name='retrieve-profile'),

    path('login/', OrganizationAuthenticationView.as_view(), name='organization-login'),

    path('organization/', OrganizationDatabaseView.as_view(), name='org-db'),
    path('organization/user/', CreateClientUser.as_view(), name='org-user-create'),
    path('organization/domain/', CreateClientDomain.as_view(), name='org-domain'),
]
