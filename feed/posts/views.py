from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Post
from django.db.models import Q
from .serializers import PostSerializer, PostListSerializer
from rest_framework.response import Response
from rest_framework.views import APIView



class PostListView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = Post.objects.all()

        #type 별 조회
        type = self.request.query_params.get('type','all')

        if type and type.lower()!= 'all':
            type_all = Q(type='facebook') | \
                    Q(type='twitter') | \
                    Q(type='instagram') | \
                    Q(type='threads') 
            if type in ['facebook', 'twitter', 'instagram', 'threads']:
                qs = qs.filter(type=type)

            else:
                qs = qs.filter(type_all)

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


