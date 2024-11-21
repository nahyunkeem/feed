from .models import Post
from .serializers import PostSerializer, PostListSerializer, PostRetrieveSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView


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
