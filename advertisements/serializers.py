from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        request = self.context["request"]
        # ads_count = len(Advertisement.objects.filter(creator=request.user, status='OPEN'))
        ads_count = Advertisement.objects.filter(creator=request.user, status='OPEN').count()

        if request.method == 'POST' and ads_count >= 10:
            raise ValidationError('Exceeded limit of open ads (max count = 10)')
        if request.method == 'PATCH' and data['status'] == 'OPEN' and ads_count >= 10:
            raise ValidationError('Exceeded limit of open ads (max count = 10)')

        return data
