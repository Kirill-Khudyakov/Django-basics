from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from advertisements import models
from advertisements.models import Advertisement, AdvertisementStatusChoices, Favorite
from advertisements.serializers import AdvertisementSerializer, FavoriteSerializer
from advertisements.filters import AdvertisementFilter
from advertisements.permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated


class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        qs = Advertisement.objects.all()

        if user.is_authenticated:
            return qs.filter(
                models.Q(status__in=[AdvertisementStatusChoices.OPEN, AdvertisementStatusChoices.CLOSED]) |
                models.Q(status=AdvertisementStatusChoices.DRAFT, creator=user)
            )
        else:
            return qs.filter(status=AdvertisementStatusChoices.OPEN)


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
