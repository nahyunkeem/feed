from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Post
from django.db import models
from .serializers import PostSerializer, PostListSerializer
from rest_framework.response import Response
from rest_framework.views import APIView



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
        


class PostListAPIView(APIView):
    def get(self, request):
        query = request.GET.get('search')
        posts = Post.objects.all()

        if query:
            posts = posts.filter(content__icontains=query)

        else:
            posts = Post.objects.all()

        if posts.exists():
            serializer = PostListSerializer(posts, many=True)
            return Response(serializer.data)
        return Response({"message": "검색된 게시물이 없습니다."})


