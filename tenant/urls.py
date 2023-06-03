from django.urls import path

from .views import CreateOrganizationUser, CreateOrganizationUserProfile, UserActivationView

app_name = 'tenant'
urlpatterns = [
    path('organization-users/', CreateOrganizationUser.as_view(), name='organization-user-create'),
    path('organization-profile/', CreateOrganizationUserProfile.as_view(), name='organization-profile-create'),
    path('organization-activate/', UserActivationView.as_view(), name='organization-user-activation'),
]
