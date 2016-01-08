from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedSimpleRouter
# from rest_framework_nested import routers
from .viewsets import BucketlistViewSet, UserViewSet, ItemViewSet
import views

root_router = DefaultRouter()

# router.register(r'bucketlists', BucketlistViewSet)
# router.register(r'auth', UserViewSet)
# router.register(r'items', ItemViewSet)

# items_router = routers.NestedSimpleRouter(
#     router, r'bucketlists', lookup='bucketlist'
# )

# items_router.register(r'items', ItemViewSet, base_name='bucketlist-items')


# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^', include(items_router.urls)),
#     url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
# ]

router = ExtendedSimpleRouter()


(
    router.register(r'bucketlists', BucketlistViewSet, base_name='bucketlist')
          .register(r'items',
                    ItemViewSet,
                    base_name='bucketlist-items',
                    parents_query_lookups=['bucketlist']
                    )
)
router.register(r'auth', UserViewSet, base_name='auth')
router.register(r'items', ItemViewSet, base_name='items')

# urlpatterns = router.urls

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
]
