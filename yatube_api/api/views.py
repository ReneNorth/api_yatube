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

    def perform_create(self, request):
        post_id = self.kwargs.get('id')
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            print(self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('id'))
        self.check_object_permissions(self.request, post)
        self.queryset = Comment.objects.filter(post_id=post.id)
        return self.queryset


# class CommentsViewSet(viewsets.ViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentsSerializer

#     def list(self, request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         queryset = Comment.objects.filter(post_id=post.id)
#         serializer = CommentsSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def create(self, request, pk):
#         post_id = self.kwargs.get('pk')
#         serializer = CommentsSerializer(data=request.data)
#         if serializer.is_valid():
#             self.request.data._mutable = True
#             self.request.data['post'] = post_id
#             self.request.data._mutable = False
#             serializer.save(author=self.request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class CommentsRetDelPatchViewSet(viewsets.ViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentsSerializer
#     permission_classes = [AuthorOrReadOnly, ]

#     def retrieve(self, request, id, pk):
#         comment = get_object_or_404(self.queryset, id=id)
#         self.check_object_permissions(request, comment)
#         serializer = CommentsSerializer(comment)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def destroy(self, request, id, pk):
#         comment = get_object_or_404(self.queryset, id=id)
#         self.check_object_permissions(request, comment)
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def partial_update(self, request, id, pk):
#         comment = get_object_or_404(self.queryset, id=id)
#         serializer = CommentsSerializer(comment,
#                                         data=request.data,
#                                         partial=True)
#         self.check_object_permissions(request, comment)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,
#                             status=status.HTTP_200_OK)
#         return Response(serializer.errors,
#                         status=status.HTTP_400_BAD_REQUEST)
