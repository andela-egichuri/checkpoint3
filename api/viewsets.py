from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework import filters
from .permissions import IsOwner
from .models import Bucketlist, Item
from .serializers import UserSerializer, BucketlistSerializer, ItemSerializer


class UserViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """User model viewset."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class BucketlistViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """Bucketlist model viewset."""

    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (IsOwner, permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')

    def perform_create(self, serializer):
        """Save bucketlist owner as current user."""
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        """Limit bucketlists to those belonging to the current user"""
        user = self.request.user
        if user.is_active:
            return user.bucketlists.all()
        return Bucketlist.objects.all()


class ItemViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """Item model viewset."""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsOwner, permissions.IsAuthenticated,)

