from rest_framework import serializers

from .models import User


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
