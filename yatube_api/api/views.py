import requests

from rest_framework import viewsets
from rest_framework import mixins
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Group, Post, Comment
from .serializers import PostSerializer, GroupSerializer


User = get_user_model()

# создать / получить лист постов
class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    pass

# получить объект или лист объектов (для групп)
class RetrieveDeleteUpdateViewSet(mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    pass

# получить редактировать или удалить
class RetrieveViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    pass


class CreateRetrieveListPostViewSet(CreateRetrieveListViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LightGroupViewSet(RetrieveViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class RetrieveDeleteUpdatePostViewSet(RetrieveDeleteUpdateViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer