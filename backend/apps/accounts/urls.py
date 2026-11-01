from django.urls import path

from .views.auth import (
    LoginView, LogoutView, MeView, PasswordChangeView, RegisterView, TokenRefreshView,
)
from .views.invitation import InvitationAcceptView, InvitationCreateView
from .views.oauth import GoogleCallbackView, GoogleLoginView
from .views.organization import (
    OrganizationDetailView, OrganizationListCreateView,
    OrganizationMemberDetailView, OrganizationMemberListView,
)

app_name = "accounts"

urlpatterns = [
    # Auth
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("auth/password/change/",
         PasswordChangeView.as_view(), name="password-change"),
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),
    path("auth/google/callback/",
         GoogleCallbackView.as_view(), name="google-callback"),
    path("auth/invitations/accept/",
         InvitationAcceptView.as_view(), name="invitation-accept"),

    # Organizations
    path("organizations/", OrganizationListCreateView.as_view(), name="org-list"),
    path("organizations/<uuid:org_id>/",
         OrganizationDetailView.as_view(), name="org-detail"),
    path("organizations/<uuid:org_id>/members/",
         OrganizationMemberListView.as_view(), name="org-members"),
    path("organizations/<uuid:org_id>/members/<uuid:member_id>/",
         OrganizationMemberDetailView.as_view(), name="org-member-detail"),
    path("organizations/<uuid:org_id>/invitations/",
         InvitationCreateView.as_view(), name="org-invitations"),
]
