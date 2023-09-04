from foods.models import Food, Discount
from accounts.models import User

from .models import Order, OrderItem


def _get_food_discount(food: Food, quantity: int) -> float:
    calc_func = {
        Discount.DiscountType.FIXED: lambda n, food: n,
        Discount.DiscountType.PERCENTAGE: lambda n, food: n * food.price / 100,
    }

    off = 0
    for discount in Discount.objects.filter(food=food):
        if not discount.is_expired():
            off += calc_func[discount.discount_type](discount.amount, food)

    return min(round(off, 2), food.price) * quantity


def _set_order_item(food: Food, quantity: int, user: User) -> [float, OrderItem]:
    try:
        order_item = OrderItem.objects.get(user=user, food=food)
        old_oitp = order_item.total_price  # old Order Item Total Price

        order_item.quantity = quantity
        order_item.total_price = food.price * quantity
        order_item.discount = _get_food_discount(food, quantity)
        order_item.save()

    except OrderItem.DoesNotExist:
        order_item = OrderItem.objects.create(
            food=food,
            quantity=quantity,
            total_price=food.price * quantity,
            discount=_get_food_discount(food, quantity),
            user=user,
        )
        old_oitp = 0

    return old_oitp, order_item


def get_cart(user: User) -> Order:
    return Order.objects.get_or_create(user=user, status=Order.Status.IN_CART[0])[0]


def update_order(food: Food, quantity: float, user: User) -> [Order, OrderItem]:
    order = get_cart(user)
    old_oitp, order_item = _set_order_item(food, quantity, user)

    order.final_price -= old_oitp
    order.final_price += order_item.total_price
    order.order_items.add(order_item)
    order.save()
    return order, order_item
