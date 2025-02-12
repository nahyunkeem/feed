from django.shortcuts import get_object_or_404
from .models import Like, Post
from .serializers import PostSerializer, PostListSerializer, PostRetrieveSerializer
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
import requests


class PostListView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        # 기본적으로는 모든 게시물을 가져옴
        qs = Post.objects.all()
        # type 별 조회
        type = self.request.query_params.get('type', 'all')
        # 타입이 all이 아니고, 정해져있다면 해당 타입으로 필터
        if type != 'all' and type in PostSerializer.AllType.values:
            qs = qs.filter(type=type)

        return qs


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.GET.get('search')

        if query:
            queryset = queryset.filter(content__icontains=query)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response([{
                "title": None,
                "content": None,
                "created_at": None,
            }])

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()  # 조회할 모델의 전체 쿼리셋을 설정
    serializer_class = PostRetrieveSerializer
    
    def get(self, request, *args, **kwargs):
        # 조회되는 Post 객체 가져오기
        post = self.get_object()
        
        # view_count 증가시키기
        post.view_count += 1
        post.save()  # 변경 사항 저장
        
        # 기본 RetrieveAPIView의 get() 메서드 호출하여 응답 반환
        return super().get(request, *args, **kwargs)



class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_count'

    def get_paginated_response(self, data):
        return Response({
            'pages': self.page.paginator.num_pages,
            'page': self.page.number,
            'post': data,
        })


class CustomOrdering(OrderingFilter):
    ordering_param = 'order_by'
    ordering_fields = ['created_at', 'updated_at', 'like_count', 'share_count', 'view_count ']
    ordering = ['-created_at']


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, CustomOrdering]
    search_fields = ['title', 'content']
    pagination_class = CustomPagination
    
 
# 게시물 좋아요 기능
class PostLike(APIView):
    permission_classes = [IsAuthenticated]    # 인증된 사용자만 접근 가능
    # POST 요청 (좋아요/좋아요 취소)

    def post(self, request, pk):
        # 게시물 가져오기
        post = get_object_or_404(Post, id=pk)
        # 좋아요 요청한 유저의 이전 기록 확인
        like, created = Like.objects.get_or_create(   # created_at 과는 다름
            user_id=request.user,
            post_id=post
        )

        if like.is_like:
            # 이미 좋아요를 눌렀다면 취소
            like.is_like = False
            like.save()
            post.like_count = max(0, post.like_count - 1)
            post.save(update_fields=['like_count'])  # 변경된 필드만 저장하는 것 추가
            return Response({"message": "좋아요 취소", "like_count": post.like_count}, status=200)

        # 좋아요 처리
        like.is_like = True
        like.save()
        post.like_count += 1
        post.save(update_fields=['like_count'])  # 변경된 필드만 저장하는 것 추가

        # 타입 api 가져오기
        if not self.type_like(type, post.content_id):
            return Response(
                {"error": f"{type} 좋아요 처리에 실패했습니다."},
                status=503
            )

        return Response({"message": "좋아요 완료", "like_count": post.like_count}, status=200)

    # type을 좋아요와 동기화
    def type_like(self, type, content_id):

        endpoints = {
            'facebook': 'https://www.facebook.com/likes/',
            'twitter': 'https://www.twitter.com/likes/',
            'instagram': 'https://www.instagram.com/likes/',
            'threads': 'https://www.threads.net/likes/',
        }
        # 타입이 지정되지 않았다면 넘기고,
        if type not in endpoints:
            return True

        try:
            # 해당 타입 api에 좋아요 요청
            response = requests.post(f"{endpoints[type]}{content_id}")
            return response.status_code == 200
        # e는 요청 중 발생할 수 있는 모든 예외(에러)를 의미
        except requests.RequestException as e:
            print(f"ERROR: SNS API 호출 실패 - {e}")
            return False


# 공유 기능
class PostShare(APIView):
    permission_classes = [IsAuthenticated]    # 인증된 사용자만 접근 가능

    def post(self, request, pk):
        # 게시물 가져오기
        post = get_object_or_404(Post, id=pk)

        # 공유 타입 가져오기
        share_type = request.data.get('type')
        # 타입 api 가져오기
        if not self.type_share(share_type, post.content_id):
            return Response(
                {"error": f"{share_type} 공유 처리에 실패했습니다."},
                status=503
            )
        # 공유를 했다면 공유 수 증가
        post.share_count += 1
        post.save(update_fields=['share_count'])

        return Response({"message": "공유 완료", "share_count": post.share_count}, status=200)

    # type을 공유와 동기화
    def type_share(self, type, content_id):

        endpoints = {
            'facebook': 'https://www.facebook.com/share/',
            'twitter': 'https://www.twitter.com/share/',
            'instagram': 'https://www.instagram.com/share/',
            'threads': 'https://www.threads.net/share/',
        }
        # 타입이 지정되지 않았다면 true 반환
        if type not in endpoints:
            return True

        try:
            # 해당 타입 api에 좋아요 요청
            response = requests.post(f"{endpoints[type]}{content_id}")
            return response.status_code == 200
        # e는 요청 중 발생할 수 있는 모든 예외(에러)를 의미
        except requests.RequestException as e:
            print(f"ERROR: SNS API 호출 실패 - {e}")
            return False
