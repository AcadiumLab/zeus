from django.urls import path

from .views import CreateOrganizationUser, CreateOrganizationUserProfile, RetrieveOrganizationView, \
    RetrieveOrganizationProfile
from .views.activation_view import UserActivationView
from .views.authentication_view import OrganizationAuthenticationView

app_name = 'tenant'
urlpatterns = [
    path('organization-users/create/', CreateOrganizationUser.as_view(), name='organization-user-create'),
    path('organization-profile/update/', CreateOrganizationUserProfile.as_view(), name='organization-profile-create'),
    path('organization-activate/', UserActivationView.as_view(), name='organization-user-activation'),

    path('organization-user/', RetrieveOrganizationView.as_view(), name='retrieve-organization'),
    path('organization-profile/', RetrieveOrganizationProfile.as_view(), name='retrieve-profile'),

    path('login/', OrganizationAuthenticationView.as_view(), name='organization-login'),
]
