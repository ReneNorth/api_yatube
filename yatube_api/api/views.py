import requests
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


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


#  перенести queryset из функций в класс
class RetrieveDeleteUpdatePostViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def destroy(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        if request.user == post.author:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if request.user == serializer.instance.author:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if request.user == serializer.instance.author:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentsViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        queryset = Comment.objects.filter(post_id=post.id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsRetDelPatchViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def retrieve(self, request, id, pk):
        comment = get_object_or_404(self.queryset, id=id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, id, pk):
        comment = get_object_or_404(self.queryset, id=id)
        if request.user == comment.author:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, id, pk):
        comment = get_object_or_404(self.queryset, id=id)
        serializer = CommentSerializer(comment,
                                       data=request.data,
                                       partial=True)
        if request.user == comment.author:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
