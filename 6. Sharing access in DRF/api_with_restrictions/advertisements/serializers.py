from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices, Favorite


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
                  'status', 'created_at', 'updated_at')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        request = self.context.get("request")
        user = request.user if request else None

        status = data.get("status", AdvertisementStatusChoices.OPEN)

        if status == AdvertisementStatusChoices.OPEN and user.is_authenticated:
            instance = getattr(self, 'instance', None)
            qs = Advertisement.objects.filter(creator=user, status=AdvertisementStatusChoices.OPEN)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.count() >= 10:
                raise serializers.ValidationError("У вас не может быть больше 10 открытых обьявлений.")
            
        return data
    

class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'advertisement')

        def validate(self, data):
            user = self.context['request'].user
            advertisement = data['advertisement']

            if advertisement.creator == user:
                raise serializers.ValidationError("Вы не можете добавить свое обьявление в избранное.")
            return data 
        

        def create(self, validated_data):
            validated_data['user'] = self.context['request'].user
            return super().create(validated_data)

