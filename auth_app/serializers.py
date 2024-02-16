from auth_app.common.errors import ClientErrors
from .models import  Account
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from auth_app.common.functions import  generate_password

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = "__all__"

    def create(self, validated_data):
        password = generate_password()
        user = Account.objects.create(**validated_data)
        # user.set_password(validated_data["password"])
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Return authenticated user email
    data:
        email and password
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data["email"]
        password = data["password"]
        acc_obj = Account.objects.filter(email=data["email"])
        if not acc_obj:
            raise ClientErrors(message="Account Not Found", response_code=404)

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    raise ClientErrors(message="Account deactivate", response_code=401)
            else:
                raise ClientErrors(message="Incorrect Password", response_code=401)
        return data