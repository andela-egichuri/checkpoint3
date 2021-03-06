from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from .models import Bucketlist, Item


class ItemSerializer(serializers.ModelSerializer):
    """Item model serializer"""

    class Meta:
        model = Item
        fields = (
            'id', 'url', 'name', 'date_created',
            'date_modified', 'bucketlist', 'done'
        )

    def get_fields(self, *args, **kwargs):
        """Allow only selection of bucketlists owned by the user"""
        fields = super(ItemSerializer, self).get_fields(*args, **kwargs)
        if self.context:
            user = self.context['request'].user
            view = self.context['view']
            bucketlists = Bucketlist.objects.filter(
                created_by=user.id).values_list('id', flat=True)
            fields['bucketlist'].queryset = fields['bucketlist'].queryset.filter(
                id__in=bucketlists).all()
        return fields


class BucketlistSerializer(serializers.ModelSerializer):
    """Bucketlist model serializer"""

    items = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name'
    )
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Bucketlist
        fields = (
            'id', 'url', 'name', 'date_created',
            'date_modified', 'created_by', 'items'
        )


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    bucketlists = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='bucketlist-detail'
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
        }
        fields = (
            'id', 'url', 'username', 'first_name',
            'last_name', 'email', 'password', 'bucketlists'
        )

    def create(self, validated_data):
        """Modify data before user creation

        Enable password hashing on API endpoint
        Convert email and username to uppercase

        """
        user = User(
            email=validated_data['email'].lower(),
            username=validated_data['username'].lower()
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """Modify data when updating user

        Enable password hashing on API endpoint
        Convert email and username to uppercase

        """
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.email = validated_data.get('email', instance.email).lower()

        instance.username = validated_data.get(
            'username', instance.username).lower()

        instance.save()
        return instance
