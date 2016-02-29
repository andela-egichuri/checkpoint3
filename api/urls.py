from django.conf.urls import include, url
from rest_framework_extensions.routers import ExtendedSimpleRouter
from .viewsets import BucketlistViewSet, UserViewSet, ItemViewSet
from api.views import api_root

router = ExtendedSimpleRouter()


(
    router.register(r'bucketlists', BucketlistViewSet)
          .register(r'items',
                    ItemViewSet,
                    base_name='bucketlist-items',
                    parents_query_lookups=['bucketlist']
                    )
)
router.register(r'users', UserViewSet)
router.register(r'items', ItemViewSet)

urlpatterns = [
    url(r'^$', api_root),
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
]
