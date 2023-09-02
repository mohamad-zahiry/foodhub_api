from rest_framework import serializers

from .models import Food, Ingredient


class IngredientSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("name",)


class FoodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    ingredients = IngredientSerializer(many=True, queryset=Ingredient.objects.all())
    category = serializers.CharField(max_length=1)
    image = serializers.ImageField()

    class Meta:
        model = Food
        fields = "__all__"

    def validate_category(self, value):
        if value not in Food.Category.values:
            raise ValueError({"category": ['category "%s" is not a value category' % value]})
        return value


class FoodUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    category = serializers.CharField(max_length=1, required=False)
    ingredients = IngredientSerializer(many=True, queryset=Ingredient.objects.all(), required=False)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(required=False, max_digits=5, decimal_places=2)
    image = serializers.ImageField(required=False)
    is_in_menu = serializers.BooleanField(required=False)

    class Meta:
        model = Food
        exclude = ("id",)

    def validate(self, attrs):
        if len(attrs["ingredients"]) == 0:
            attrs.pop("ingredients")

        return attrs
