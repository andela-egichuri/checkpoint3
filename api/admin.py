from django.contrib import admin
from .models import Bucketlist, Item


class ItemInline(admin.TabularInline):
    model = Item


class BucketlistAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'date_created', 'date_modified', 'created_by'
    )
    inlines = [
        ItemInline,
    ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'date_created', 'date_modified', 'done', 'bucketlist'
    )


admin.site.register(Bucketlist, BucketlistAdmin)

admin.site.register(Item, ItemAdmin)
