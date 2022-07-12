import django.db.utils
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.users.error_codes import AccountErrorCodes
from apps.users.models import Company
from project import settings


def create_user(validated_data):
    validated_data.pop('confirm_password')
    validated_data['username'] = validated_data['email']
    instance = get_user_model().objects.create(**validated_data)
    instance.set_password(validated_data['password'])
    instance.save()
    return instance


class AuthRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only=True, min_length=6)

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'id': {'read_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True, 'min_length': 6},
        }

    def validate_confirm_password(self, val):
        password = self.initial_data['password']
        if val != password:
            raise ValidationError(AccountErrorCodes.PASSWORD_MISMATCH)

    @transaction.atomic
    def create(self, validated_data):
        try:
            user = create_user(validated_data)
            if settings.VERIFY_EMAIL:
                user.is_active = False
                user.save()
                user.generate_email_verification_code()
            return user
        except django.db.utils.IntegrityError:
            # todo: Add logger to log the exception
            raise ValidationError(AccountErrorCodes.USER_EXIST)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    company = CompanySerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'first_name', 'last_name', 'email', 'password', 'company', 'phone', 'role'
        ]

    def create(self, validated_data):
        try:
            return create_user(validated_data)
        except django.db.utils.IntegrityError:
            raise django.db.utils.IntegrityError(AccountErrorCodes.USER_EXIST)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data.pop('password')
        if 'email' in validated_data:
            validated_data['username'] = validated_data['email']
        return super().update(instance, validated_data)


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    confirm_new_password = serializers.CharField(required=True, min_length=6)

    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password', 'confirm_new_password']

    def validate_confirm_new_password(self, val):
        password = self.initial_data['new_password']
        if val != password:
            raise ValidationError(AccountErrorCodes.PASSWORD_MISMATCH)

    def update(self, instance, validated_data):
        if instance.check_password(validated_data['old_password']):
            instance.set_password(validated_data['new_password'])
            return instance
        else:
            raise ValidationError(AccountErrorCodes.INVALID_PASSWORD)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone']


class UserRequestResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    confirm_new_password = serializers.CharField(required=True, min_length=6)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.user = get_object_or_404(get_user_model(), email=self.initial_data['email'])
        except Http404:
            raise ValidationError(AccountErrorCodes.UNKNOWN_USER)

    def validate_confirm_new_password(self, val):
        password = self.initial_data['new_password']
        if val != password:
            raise ValidationError(AccountErrorCodes.PASSWORD_MISMATCH)

    def validate_token(self, val):
        if not default_token_generator.check_token(self.user, val):
            raise ValidationError(AccountErrorCodes.UNKNOWN_USER)

    class Meta:
        model = get_user_model()
        fields = ['new_password', 'confirm_new_password', 'token', 'email']
