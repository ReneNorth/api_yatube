from posts.models import Comment, Group, Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')
        read_only_fields = ('author', 'pub_date', 'author', 'id')
        extra_kwargs = {'slug': {'required': True}, 'text': {'required': True}}


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'slug', 'title', 'description')
        read_only_fields = ('id',)
        extra_kwargs = {'slug': {'required': True}}


class CommentsSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(many=False,
                                              queryset=Post.objects.all())
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author',)
        extra_kwargs = {'text': {'required': True}}
