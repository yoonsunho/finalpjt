from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
# Permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count,Exists, OuterRef,Value,Q

from django.shortcuts import get_object_or_404

from .models import Article, Comment, Like
from .serializers import ArticleSerializer, CommentSerializer, LikeSerializer


# Create your views here.
# 게시글 목록 조회 및 작성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_list_create(request):
    # 게시글 조회
    if request.method == 'GET':
        # 현재 사용자 (로그인 여부 확인)
        user = request.user if request.user.is_authenticated else None

        # 1. 필수 필터링 파라미터 (기본값: REVIEW)
        category = request.GET.get('category', 'REVIEW')  # 기본 카테고리 설정
        ordering = request.GET.get('ordering', 'latest')  # 기본 정렬: 최신순

        # 2. 카테고리 유효성 검사
        if category not in dict(Article.CATEGORY_CHOICES):
            return Response(
                {"detail": "유효하지 않은 카테고리입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 3. 필수 카테고리 필터링
        queryset = Article.objects.filter(category=category)

        # 검색 기능 추가 
        search_field = request.GET.get('search_field','').strip()
        search = request.GET.get('search','').strip()

        # 검색 필드에 따라 다르게 필터링
        if search and search_field in ['title', 'content', 'nickname']:
            if search_field == 'title':
                queryset = queryset.filter(title__icontains=search)
            elif search_field == 'content':
                queryset = queryset.filter(content__icontains=search)
            elif search_field == 'nickname':
                queryset = queryset.filter(user__nickname__icontains=search)

        # annotate로 likes_count와 is_liked 추가
        queryset = queryset.annotate(
            likes_count=Count('likes'),
            is_liked=Exists(
                Like.objects.filter(
                    article=OuterRef('pk'),  # ⚠️ Like 모델의 FK가 article인지 확인!
                    user=user
                )
            ) if user else Value(False)  # 비회원은 무조건 False
        ).select_related('user')

        # 5. 정렬
        if ordering == 'latest':
            queryset = queryset.order_by('-created_at')
        elif ordering == 'oldest':
            queryset = queryset.order_by('created_at')
        elif ordering == 'popular':
            queryset = queryset.order_by('-likes_count', '-created_at')
        else:
            queryset = queryset.order_by('-created_at')  # 기본값: 최신순

        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # 작성
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 게시글 상세 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE',])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_detail(request, article_id):
    # article = get_object_or_404(Article, id=article_id)

    # 현재 사용자 (로그인 여부 확인)
    user = request.user if request.user.is_authenticated else None

    # annotate로 likes_count와 is_liked 추가
    article = get_object_or_404(
        Article.objects.annotate(
            likes_count=Count('likes'),
            is_liked=Exists(
                Like.objects.filter(
                    article=OuterRef('pk'),  # ⚠️ Like 모델의 FK가 article인지 확인!
                    user=user
                )
            ) if user else Value(False)  # 비회원은 무조건 False
        ),
        id=article_id
    )

    if request.method == 'GET':
        article.likes_count = article.likes.count()
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if article.user != request.user:
            return Response({"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        if article.user != request.user:
            return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 게시글 좋아요/취소 (토글)
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_like(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    like, created = Like.objects.get_or_create(user=request.user, article=article)
    if created:
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        like.delete()
        return Response({"detail": "좋아요가 취소되었습니다."}, status=status.HTTP_204_NO_CONTENT)

# 댓글 목록 조회 및 작성 (대댓글 지원)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list_create(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'GET':
        comments = Comment.objects.filter(article=article, parent__isnull=True).select_related('user')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    #
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            parent_id = request.data.get('parent')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                serializer.save(user=request.user, article=article, parent=parent_comment)
            else:
                serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 댓글 수정 및 삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'PUT':
        if comment.user != request.user:
            return Response({"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if comment.user != request.user:
            return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)