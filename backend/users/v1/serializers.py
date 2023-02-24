from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
    model = User
    read_only_fields = ['id', 'is_subscribed']

    def validate_is_subscribed(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                'You can not subscribe to yourself'
            )
        return value

    def get_is_subscribed(self, obj):
        request = self.context['request']
        if request.user:
            # The condition in the `filter` covers both situations:
            # when user is authorized and anonymous,
            # in comparison with the condition `user=request.user`,
            # that falls with the error in the case of an
            # anonymous client.
            return obj.subscribing.filter(user__id=request.user.id).exists()
        else:
            return False


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        model = User
        read_only_fields = ['id']
