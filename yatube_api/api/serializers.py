from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from posts.models import Group, Post, Comment


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    
    # чтобы получить строковое представление вместо ID
    author = serializers.StringRelatedField(read_only=True)
    #author = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('text', 'pub_date', 'author', 'group', 'id', 'comments')
        read_only_fields = ('author',)
        extra_kwargs = {'slug': {'required': True}, 'text': {'required': True}}
        
    #def get_author(self, obj):
    #    return obj.username
        


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'slug', 'title', 'description')
        extra_kwargs = {'slug': {'required': True}}



class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(many=False, queryset=Post.objects.all())
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        #fields = ('created', 'post',)
        fields = ('text', 'created', 'author', 'post', 'id')
        read_only_fields = ('author',)
        extra_kwargs = {'post': {'required': True}}
        # extra_kwargs = {'text': {'required': True}, 'post': {'required': True}}
        
    
        
        
        
