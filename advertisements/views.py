from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import AdvertisementFilter
from .models import Advertisement
from .permissions import IsOwnerOrReadOnly
from .serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []

    def get_queryset(self):
        us = self.request.user
        queryset = Advertisement.objects.exclude(status="DRAFT")
        queryset_draft = Advertisement.objects.filter(status="DRAFT", creator=us.id)
        if self.request.user.is_authenticated:
            queryset = queryset or queryset_draft
        return queryset.order_by('id')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(methods=['post'], detail=True, url_path='toggle_favorite')
    def favorite(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        if user.favorites.filter(id=post.id).exists():
            user.favorites.remove(post)
        else:
            if post.creator != user:
                user.favorites.add(post)
        return Response({'status': user.favorites.filter(id=post.id).exists()})
