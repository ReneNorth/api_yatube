from api.views import (CommentsRetDelPatchViewSet, CommentsRetDelPatchViewSet,
                       CreateRetrieveListPostViewSet, LightGroupViewSet,
                       RetrieveDeleteUpdatePostViewSet)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('posts', CreateRetrieveListPostViewSet)
router.register('groups', LightGroupViewSet)
# router.register(r'comments',
#                 CommentsRetDelPatchViewSet,
#                 basename='CommentsRetDelPatchViewSet')
router.register(
    r'posts/(?P<id>\d+)/comments',
    CommentsRetDelPatchViewSet)
router.register(
    r'posts',
    RetrieveDeleteUpdatePostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/posts/<int:pk>/comments/<int:id>/',
    #      CommentsRetDelPatchViewSet.as_view(
    #          {'get': 'retrieve',
    #           'delete': 'destroy',
    #           'patch': 'partial_update'}
    #      )),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('api/v1/', include(router.urls)),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
