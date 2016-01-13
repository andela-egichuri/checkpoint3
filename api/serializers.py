from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bucketlist, Item


class ItemSerializer(serializers.ModelSerializer):
    """Item model serializer"""

    bucketlist = serializers.ReadOnlyField(
        source='bucketlist.name'
    )

    class Meta:
        model = Item
        fields = (
            'url', 'name', 'date_created',
            'date_modified', 'bucketlist', 'done'
        )


class BucketlistSerializer(serializers.ModelSerializer):
    """Bucketlist model serializer"""

    items = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name'
    )
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Bucketlist
        fields = (
            'url', 'name', 'date_created',
            'date_modified', 'created_by', 'items'
        )


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    bucketlists = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='bucketlist-detail'
    )

    class Meta:
        model = User
        write_only_fields = ('password', 'email')
        fields = (
            'url', 'username', 'first_name',
            'last_name', 'email', 'password', 'bucketlists'
        )

    def create(self, validated_data):
        """Enable password hashing on API endpoint"""
        user = User(
            email=validated_data['email'], username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
