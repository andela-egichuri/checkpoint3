from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework_extensions.mixins import NestedViewSetMixin
from permissions import IsOwner
from .models import Bucketlist, Item
from .serializers import UserSerializer, BucketlistSerializer, ItemSerializer


class UserViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """User model viewset"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BucketlistViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """Bucketlist model viewset"""
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (IsOwner, permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_active:
            return user.bucketlists.all()
        return Bucketlist.objects.all()


class ItemViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """Item model viewset"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsOwner, permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        bucketlists = Bucketlist.objects.filter(created_by=user.id)
        if user.is_active:
            return Item.objects.filter(bucketlist__in=bucketlists)
        return Item.objects.all()
