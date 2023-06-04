from django.urls import path

from .views import CreateOrganizationUser, CreateOrganizationUserProfile, RetrieveOrganizationView, \
    RetrieveOrganizationProfile
from .views.activation_view import UserActivationView
from .views.authentication_view import OrganizationAuthenticationView
from .views.client_view import CreateOrganizationDatabaseView, ListOrganizationDatabaseView, CreateClientUser

app_name = 'tenant'
urlpatterns = [
    path('organization-user/create/', CreateOrganizationUser.as_view(), name='organization-signup'),
    path('organization-profile/update/', CreateOrganizationUserProfile.as_view(), name='organization-profile-create'),
    path('organization-activate/', UserActivationView.as_view(), name='organization-user-activation'),

    path('organization-user/', RetrieveOrganizationView.as_view(), name='retrieve-organization'),
    path('organization-profile/', RetrieveOrganizationProfile.as_view(), name='retrieve-profile'),

    path('login/', OrganizationAuthenticationView.as_view(), name='organization-login'),

    path('organization-db/create', CreateOrganizationDatabaseView.as_view(), name='organization-db-create'),
    path('organization-db/user/create', CreateClientUser.as_view(), name='organization-user-create'),
    path('organization-db/list', ListOrganizationDatabaseView.as_view(), name='organization-db-list'),
]
