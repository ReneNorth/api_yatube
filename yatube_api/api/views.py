from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .serializers import CommentsSerializer, GroupSerializer, PostSerializer
from .permissions import AuthorOrReadOnly, CommentsPermission


class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    pass


class RetrieveDeleteUpdateViewSet(mixins.RetrieveModelMixin,
                                  mixins.DestroyModelMixin,
                                  mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    pass


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


class RetrieveDeleteUpdatePostViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AuthorOrReadOnly, ]

    def retrieve(self, request, pk):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        self.check_object_permissions(request, post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentsRetDelPatchViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [CommentsPermission, ]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('id'))
        self.check_object_permissions(self.request, post)
        self.queryset = Comment.objects.filter(post_id=post.id)
        return self.queryset
