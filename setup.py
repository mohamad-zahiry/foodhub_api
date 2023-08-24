from django import setup

setup()


from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.constants import ALL_PERMISSIONS, PERMISSIONS_CONTENT_TYPE, GROUPS_PERMISSIONS


permissions = {}

for p_codename, p_name in ALL_PERMISSIONS.items():
    app_label, model = PERMISSIONS_CONTENT_TYPE[p_codename]
    content_type = ContentType.objects.get(app_label=app_label, model=model)
    perm = Permission.objects.create(
        name=p_name,
        codename=p_codename,
        content_type=content_type,
    )
    print(f'permission "{p_name}" created')
    permissions[p_codename] = perm


for group, perms in GROUPS_PERMISSIONS.items():
    _group = Group.objects.create(name=group)
    print(f'group "{group}" created with permissions:')
    for perm in perms:
        print(f"  {ALL_PERMISSIONS[perm]}")
        _group.permissions.add(permissions[perm])
