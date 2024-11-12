from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Post
from django.db.models import Q
from .serializers import PostSerializer


# Create your views here.
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
        
