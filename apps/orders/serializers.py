from rest_framework import serializers

from foods.models import Food

from .utils import update_order
from .models import OrderItem


class ShortFoodSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ("id", "name")


class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    food = ShortFoodSerializer(queryset=Food.objects.all())
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    discount = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderItem
        fields = ("id", "food", "quantity", "total_price", "discount")

    def create(self, validated_data):
        order, order_item = update_order(
            food=validated_data["food"],
            quantity=validated_data["quantity"],
            user=self.context["user"],
        )
        return order_item
