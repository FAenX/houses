from django.urls import path, include

from .views import (
    base, tenant, landlord, moderator
)


urlpatterns = [
     # accounts
     path('accounts/', include('django.contrib.auth.urls')),
     path('accounts/signup/', base.UserSignUpView.as_view(), name='signup'),
     path('tenant/signup/', tenant.TenantSignupView.as_view(), name='tenant_signup'),
     path('landlord/signup/', landlord.LandlordSignupView.as_view(), name='landlord_signup'),
     
     


]