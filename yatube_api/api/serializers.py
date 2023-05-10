from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username', required=True, queryset=User.objects.all())

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate(self, data):
        current_user = self.context['request'].user
        author = data.get('following')
        follow_record = Follow.objects.filter(
            user=current_user, following=author
        )
        if current_user == author or follow_record.exists():
            raise ValidationError('Нельзя подписываться на самого себя, или '
                                  'подписываться на одного и того же автора')

        return data
