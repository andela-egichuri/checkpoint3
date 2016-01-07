from django.contrib import admin
from .models import Bucketlist, Item


class BucketlistAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'date_created', 'date_modified', 'created_by'
    )


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'date_created', 'date_modified', 'done', 'bucketlist'
    )


admin.site.register(Bucketlist, BucketlistAdmin)

admin.site.register(Item, ItemAdmin)
