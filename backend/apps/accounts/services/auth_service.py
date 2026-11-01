from django.db import transaction

from apps.accounts.models import Membership, Organization, User


@transaction.atomic
def register_user(*, email, password, organization_name, first_name="", last_name=""):
    user = User.objects.create_user(
        email=email, password=password, first_name=first_name, last_name=last_name
    )
    org = Organization.objects.create(name=organization_name)
    Membership.objects.create(
        user=user, organization=org, role=Membership.Role.OWNER)
    return user, org
