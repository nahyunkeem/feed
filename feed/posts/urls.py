from django.urls import path
from .views import PostListView, PostListAPIView, PostLike, PostShare

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("search", PostListAPIView.as_view()),
    path("likes/<int:pk>", PostLike.as_view(), name="post_likes"),
    path("share/<int:pk>", PostShare.as_view(), name="post_share"),
]
