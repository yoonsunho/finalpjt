from rest_framework import serializers
from .models import Article, Comment, Like

class ArticleSerializer(serializers.ModelSerializer):
    
    likes_count = serializers.IntegerField(read_only=True)  # annotate 결과 사용
    user = serializers.ReadOnlyField(source = 'user.nickname')
    
    class Meta:
        model = Article
        fields = '__all__'
    
# 대댓글 지원
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = Comment
        fields = (
            'id', 'user', 'content', 'created_at', 
            'updated_at', 'parent', 'replies'
        )
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj)
        return CommentSerializer(replies, many=True).data
    

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'article', 'created_at')
        read_only_fields = ['user', 'created_at']
        extra_kwargs = {
            'article': {'required': True}
        }