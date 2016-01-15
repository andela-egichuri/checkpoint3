from rest_framework import permissions
from .models import Item


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Item):
            return obj.bucketlist.created_by == request.user
        return obj.created_by == request.user
