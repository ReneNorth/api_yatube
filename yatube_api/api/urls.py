from api.views import (CommentsRetDelPatchViewSet, LightGroupViewSet,
                       RetrieveDeleteUpdatePostViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('posts', RetrieveDeleteUpdatePostViewSet)
router.register('groups', LightGroupViewSet)
router.register(r'posts/(?P<id>\d+)/comments',
                CommentsRetDelPatchViewSet,
                basename='comments')

urlpatterns = [
    path('api/v1/', include(router.urls))
]
