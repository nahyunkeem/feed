from .models import Post
from .serializers import PostSerializer, PostListSerializer
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination


class PostListView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        # 기본적으로는 모든 게시물을 가져옴
        qs = Post.objects.all()
        # type 별 조회
        type = self.request.query_params.get('type','all')
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