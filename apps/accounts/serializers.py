from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from .models import User, Address
from .utils import change_group


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password_1 = serializers.CharField(write_only=True)
    new_password_2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("old_password", "new_password_1", "new_password_2")

    def validate(self, attrs):
        if attrs["new_password_1"] != attrs["new_password_2"]:
            raise serializers.ValidationError(
                {"new_password_2": "new_password_1 and new_password_2 is not equal"}
            )
        return super().validate(attrs)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "old_password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password_1"])
        instance.save()
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    phone = PhoneNumberField()

    class Meta:
        model = User
        fields = ("email", "name", "phone")


class ChangeGroupSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        fields = ("email", "group")

    def validate(self, attrs):
        try:
            attrs["email"] = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "user does not exist"})
        return super().validate(attrs)

    def create(self, validated_data):
        change_group(
            sender=self.context.get("sender"),
            user=validated_data["email"],
            group=self.context.get("group"),
        )
        return validated_data["email"]

    def update(self, instance, validated_data):
        return instance


class AddressSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("pk", "address")


class CreateAddressSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("address",)

    def create(self, validated_data):
        validated_data["user"] = self.context["user"]
        instance = Address(**validated_data)
        instance.save()
        return instance


class UpdateDeleteAddressSerailizer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()

    class Meta:
        model = Address
        fields = ("pk", "address")

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
