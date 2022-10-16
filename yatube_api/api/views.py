from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post
from rest_framework import viewsets

from .permissions import AuthorOrReadOnly, CommentsPermission
from .serializers import CommentsSerializer, GroupSerializer, PostSerializer


class LightGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class RetrieveDeleteUpdatePostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permissions_classes = [AuthorOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'destroy' or self.action == 'partial_update':
            return [AuthorOrReadOnly(), ]
        return super().get_permissions()


class CommentsRetDelPatchViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [CommentsPermission, ]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('id'))
        self.queryset = Comment.objects.filter(post_id=post.id)
        return self.queryset
