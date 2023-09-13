from decimal import Decimal

from rest_framework.exceptions import ValidationError

from foods.models import Food, Discount
from accounts.models import User, Address
from loyalty_club.models import Coupon

from .models import Order, OrderItem


def get_food_discount(food: Food, quantity: int) -> float:
    calc_func = {
        Discount.DiscountType.FIXED: lambda n, food: n,
        Discount.DiscountType.PERCENTAGE: lambda n, food: n * food.price / 100,
    }

    off = 0
    for discount in Discount.objects.filter(food=food):
        if not discount.is_expired():
            off += calc_func[discount.discount_type](discount.amount, food)

    return min(round(off, 2), food.price) * quantity


def get_cart(user: User) -> Order:
    return Order.objects.get_or_create(user=user, state=Order.State.ORDER)[0]


def update_order(food: Food, quantity: float, user: User) -> [Order, OrderItem]:
    order = get_cart(user)
    try:
        order_item = order.order_items.get(user=user, food=food)
        # minus the old order-item price from order
        order.final_price -= order_item.total_price - Decimal(order_item.discount)

        order_item.quantity = quantity
        order_item.total_price = food.price * quantity
        order_item.discount = get_food_discount(food, quantity)
        order_item.save()

    except OrderItem.DoesNotExist:
        order_item = OrderItem.objects.create(
            food=food,
            quantity=quantity,
            total_price=food.price * quantity,
            discount=get_food_discount(food, quantity),
            user=user,
        )

    # update order-items list
    order.order_items.add(order_item)
    # update new final price
    order.final_price += order_item.total_price - Decimal(order_item.discount)
    order.save()
    return order, order_item


def delete_order_item(order_item: OrderItem):
    order = OrderItem.objects.prefetch_related("order_set").get(pk=order_item.pk).order_set.first()
    order.final_price -= order_item.total_price - Decimal(order_item.discount)
    order.save()
    order_item.delete()


def finish_order(order: Order, phone: str, address: Address, coupon: Coupon = None):
    # after finish_order, use get_payment_link in "payments.utils"
    if not order.order_items.exists():
        raise ValidationError("cart is empty")

    if order.state == Order.State.ORDER:
        order.state = Order.State.PAYMENT
        order.phone = phone
        order.address = address
        if coupon is not None:
            order.coupon = coupon
        order.save()


def update_order_price(order: Order):
    pass
