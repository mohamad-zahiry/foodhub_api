from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import DjangoModelPermissions

from constants import CAN_CHANGE_GROUP
from .models import User


def permission(*perms):
    class CustomPerm(DjangoModelPermissions):
        permissions = perms

        def get_required_permissions(self, method, model_cls):
            return self.permissions

    return CustomPerm


def _change_group(user: User, group: Group):
    user.groups.clear()
    user.groups.add(Group.objects.get(name=group))


def change_group(sender: User, user: User, group: Group):
    if user.is_staff:
        # raise PermissionDenied({"group": ["you cannot change group of a higher user"]})
        raise PermissionDenied({"group": ["you cannot change this user group"]})

    if sender.is_staff:
        return _change_group(user, group)

    sender_group = sender.groups.first()
    user_group = user.groups.first()

    if sender_group == group:
        # raise PermissionDenied({"group": ["you cannot promote a user to your group"]})
        raise PermissionDenied({"group": ["you cannot change this user group"]})

    if sender_group == user_group:
        # raise PermissionDenied({"group": ["you cannot change your groupmates info"]})
        raise PermissionDenied({"group": ["you cannot change this user group"]})

    if user_group.name not in CAN_CHANGE_GROUP[sender_group.name]:
        # raise PermissionDenied({"group": ["you cannot change group of a higher user"]})
        raise PermissionDenied({"group": ["you cannot change this user group"]})

    return _change_group(user, group)
