from api.views import (CommentsRetDelPatchViewSet, LightGroupViewSet,
                       RetrieveDeleteUpdatePostViewSet)
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('posts', RetrieveDeleteUpdatePostViewSet)
router.register('groups', LightGroupViewSet)
router.register(r'posts/(?P<id>\d+)/comments',
                CommentsRetDelPatchViewSet,
                basename='comments')

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls))
]
