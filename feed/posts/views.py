from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostListSerializer


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


    # def get(self, request, format=None):
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)

