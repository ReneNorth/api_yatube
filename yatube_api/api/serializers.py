from posts.models import Comment, Group, Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Post
        fields = ('text', 'pub_date', 'author', 'group', 'id', 'comments')
        read_only_fields = ('author',)
        extra_kwargs = {'slug': {'required': True}, 'text': {'required': True}}


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'slug', 'title', 'description')
        extra_kwargs = {'slug': {'required': True}}


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(many=False,
                                              queryset=Post.objects.all())
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('text', 'created', 'author', 'post', 'id')
        read_only_fields = ('author',)
        extra_kwargs = {'text': {'required': True}, 'post': {'required': True}}
