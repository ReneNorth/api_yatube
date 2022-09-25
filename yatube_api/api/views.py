import requests

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Group, Post, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


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



# перенести queryset из функций в класс 
class RetrieveDeleteUpdatePostViewSet(viewsets.ViewSet):
    #queryset = Post.objects.all()
    #serializer_class = PostSerializer
    
    # api/v1/posts/{post_id}/ (GET, PUT, PATCH, DELETE): 
    # получаем, редактируем или удаляем пост по id.
    
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
        # serializer = PostSerializer(post)
        
        # дописать возврат статуса об успешном удалении
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    
    
    # разобраться что не так с апдейтом
    def update(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if request.user == serializer.instance.author:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
    

    
    def partial_update(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if request.user == serializer.instance.author:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    
    

class CommentsViewSet(viewsets.ViewSet):
    
    #queryset = Comment.objects.all()
    #serializer_class = CommentSerializer
    
    
    #def get_queryset(self):
        #post_id = self.kwargs.get("post_id")
    #    post = get_object_or_404(
    #        Comment,
    #        pk=self.kwargs.get("post_id")
    #    )
    #    print(dir(post))
    #    #return Comment.objects.filter(post=post_id)
    #    return Comment.objects.filter(post=post.id)
    
    
    #@action(methods=['post'], detail=True, url_path='comments')
    def list(self, request, pk):
        print(request.data, '<-')
        
        post = get_object_or_404(Post, pk=pk)
        post_id = post.id
        print(post, '<-')
        print(post_id)
        queryset = Comment.objects.filter(post_id=post_id)
        print(queryset)
        # queryset = post.comments.all()
        # comment = 
        #post = get_object_or_404(queryset, pk=pk)
        print(queryset, 'queryset <-')
        serializer = CommentSerializer(queryset, many=True)
        print(serializer)
        return Response(serializer.data)
    
        #    queryset = Post.objects.all()
        #post = get_object_or_404(queryset, pk=pk)
        #serializer = PostSerializer(post)
        #return Response(serializer.data)
    
    
    
# https://stackoverflow.com/questions/53687071/django-rest-framework-not-null-constraint-failed    
    # как избавиться от PK? 
    def create(self, request, pk):

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """
    def destroy(self, request, pk, id):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    """
    
#    def retrieve(self, request, pk, id):
#        pass


#class RetrieveDeleteUpdateCommentViewSet(RetrieveDeleteUpdateViewSet):
#    queryset = Comment.objects.all()
#    serializer_class = CommentSerializer
    

class CommentsRetDelPatchViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def retrieve(self, request, id, pk):
        print(f'{request}')
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
        print(f'{request} <- request')
        print(f'{request.data} <- request')
        comment = get_object_or_404(self.queryset, id=id)
        print(type(comment), '<- print comment')
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        print('did we get here?')
        if request.user == comment.author:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
        