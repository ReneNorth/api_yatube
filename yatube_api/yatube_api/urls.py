from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


# from ..api.serializers import PostSerializer
from api.views import CreateRetrieveListPostViewSet, LightGroupViewSet, RetrieveDeleteUpdatePostViewSet


router = DefaultRouter()

router.register('api/v1/posts', CreateRetrieveListPostViewSet)
router.register('api/v1/groups', LightGroupViewSet)
router.register(r'api/v1/posts', RetrieveDeleteUpdatePostViewSet)
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
