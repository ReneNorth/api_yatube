from api.views import (CommentsRetDelPatchViewSet,
                       CreateRetrieveListPostViewSet,
                       LightGroupViewSet,
                       RetrieveDeleteUpdatePostViewSet)

from rest_framework.routers import DefaultRouter
from django.urls import include, path

router = DefaultRouter()

router.register(r'posts', CreateRetrieveListPostViewSet)
router.register(r'groups', LightGroupViewSet)
router.register(r'posts', RetrieveDeleteUpdatePostViewSet)
router.register(r'posts/(?P<id>\d+)/comments', CommentsRetDelPatchViewSet)

urlpatterns = [
    path('', include(router.urls))
]
