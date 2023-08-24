class PERMISSIONS:
    CHANGE_ORDER_STATUS = "change_order_status"
    CANCEL_ORDER = "cancel_order"
    ADD_CHEF = "add_chef"
    ADD_CUSTOMER = "add_customer"
    DELETE_USER = "d_user"
    ADD_DELETE_CHANGE_FOOD = "adc_food"
    ADD_DELETE_CHANGE_DISCOUNT = "adc_discount"
    ADD_DELETE_CHANGE_COUPON = "adc_coupon"
    ADD_ADMIN = "add_admin"


P = PERMISSIONS

# different groups permissions
CUSTOMER_PERMISSIONS = {}

CHEF_PERMISSIONS = {
    P.CHANGE_ORDER_STATUS: "Change order status",
    P.CANCEL_ORDER: "Cancel order",
}


ADMIN_PERMISSIONS = CHEF_PERMISSIONS.copy()
ADMIN_PERMISSIONS.update(
    {
        P.ADD_CHEF: "Add chef",
        P.ADD_CUSTOMER: "Add customer",
        P.DELETE_USER: "Delete user",
        P.ADD_DELETE_CHANGE_FOOD: "Add/delete/change food",
        P.ADD_DELETE_CHANGE_DISCOUNT: "Add/delete/change discount",
        P.ADD_DELETE_CHANGE_COUPON: "Add/delete/change coupon",
    }
)

OWNER_PERMISSIONS = ADMIN_PERMISSIONS.copy()
OWNER_PERMISSIONS.update(
    {
        P.ADD_ADMIN: "Add admin",
    }
)

ALL_PERMISSIONS = OWNER_PERMISSIONS

# each permissoin content type: (app_label, model)
PERMISSIONS_CONTENT_TYPE = {
    P.CHANGE_ORDER_STATUS: ("orders", "order"),
    P.CANCEL_ORDER: ("orders", "order"),
    P.ADD_CHEF: ("accounts", "user"),
    P.ADD_CUSTOMER: ("accounts", "user"),
    P.DELETE_USER: ("accounts", "user"),
    P.ADD_DELETE_CHANGE_FOOD: ("foods", "food"),
    P.ADD_DELETE_CHANGE_DISCOUNT: ("foods", "discount"),
    P.ADD_DELETE_CHANGE_COUPON: ("loyalty_club", "coupon"),
    P.ADD_ADMIN: ("accounts", "user"),
}

# all groups permissions
GROUPS_PERMISSIONS = {
    "customer": CUSTOMER_PERMISSIONS,
    "chef": CHEF_PERMISSIONS,
    "admin": ADMIN_PERMISSIONS,
    "owner": OWNER_PERMISSIONS,
}


class _GROUPS:
    CUSTOMER = "customer"
    CHEF = "chef"
    ADMIN = "admin"
    OWNER = "owner"

    def __iter__(self):
        return iter(GROUPS_PERMISSIONS.keys())


# groups singleton
GROUPS = _GROUPS()

# determine each group, group-changing access
CAN_CHANGE_GROUP = {
    GROUPS.CUSTOMER: [],
    GROUPS.CHEF: [],
    GROUPS.ADMIN: [GROUPS.CHEF, GROUPS.CUSTOMER],
    GROUPS.OWNER: [GROUPS.ADMIN, GROUPS.CHEF, GROUPS.CUSTOMER],
}


def perm_name(perm):
    return PERMISSIONS_CONTENT_TYPE[perm][0] + "." + perm
