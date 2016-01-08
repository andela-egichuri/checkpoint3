from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bucketlist, Item


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'url', 'username', 'first_name', 'last_name', 'email', 'password'
        )


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = (
            'name', 'date_created',
            'date_modified', 'bucketlist', 'done'
        )


class BucketlistSerializer(serializers.ModelSerializer):

    items = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name'
    )
    # items_url = serializers.HyperlinkedIdentityField(
    #     view_name='bucketlist-items-list',
    #     lookup_url_kwarg='bucketlist_pk'
    # )

    class Meta:
        model = Bucketlist
        fields = (
            'url', 'name', 'date_created',
            'date_modified', 'created_by', 'items'
        )
