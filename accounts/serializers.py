from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from .models import UserProfile


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=["student", "recruiter"])

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value.lower()

    @transaction.atomic
    def create(self, data):
        role = data.pop("role")
        password = data.pop("password")
        user = User.objects.create_user(password=password, **data)
        UserProfile.objects.create(user=user, role=role)
        return user


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]

    def get_role(self, user):
        from .permissions import get_role
        return get_role(user)
