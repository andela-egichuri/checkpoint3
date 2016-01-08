from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Bucketlist, Item
from .serializers import UserSerializer, BucketlistSerializer, ItemSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin


class UserViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BucketlistViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer


class ItemViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    # def get_queryset(self):
    #     bucketlist_id = self.kwargs.get('bucketlist_pk', None)
    #     if bucketlist_id:
    #         return Item.objects.filter(bucketlist=bucketlist_id)
    #     return super(ItemViewSet, self).get_queryset()

