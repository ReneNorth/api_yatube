from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


# from ..api.serializers import PostSerializer
from api.views import CreateRetrieveListPostViewSet, LightGroupViewSet, CommentsRetDelPatchViewSet, CommentsViewSet, RetrieveDeleteUpdatePostViewSet


router = DefaultRouter()


# переделать basename в соответствии с https://practicum.yandex.ru/trainer/backend-developer/lesson/49116c4f-4473-441e-afc2-d49d6168406e/task/2862382b-1125-42ca-9b93-72929774035e/
router.register('api/v1/posts', CreateRetrieveListPostViewSet)
router.register('api/v1/groups', LightGroupViewSet)
router.register(r'api/v1/posts/(?P<pk>\d+)/comments', CommentsViewSet, basename='CommentsViewSet')
router.register(r'api/v1/posts', RetrieveDeleteUpdatePostViewSet, basename='RetrieveDeleteUpdatePostViewSet')
# router.register(r'api/v1/posts/(?P<pk>\d+)/comments/(?P<id>\d)', RetrieveDeleteUpdateCommentViewSet, basename='RetrieveDeleteUpdateCommentViewSet')

# router.register('owners', OwnerViewSet)
# router.register(r'mycats', LightCatViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
#     # Djoser создаст набор необходимых эндпоинтов.
#    # базовые, для управления пользователями в Django:
#     path('auth/', include('djoser.urls')),
#     # JWT-эндпоинты, для управления JWT-токенами:
#     path('auth/', include('djoser.urls.jwt')),
# ]


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/v1/posts/<int:pk>/comments/<int:id>/', CommentsViewSet.as_view(({'get': 'retrieve', 'delete': 'destroy'}))),
    path('api/v1/posts/<int:pk>/comments/<int:id>/', CommentsRetDelPatchViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update'})),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
