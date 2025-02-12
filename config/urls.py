from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("feed.accounts.urls")),
    path("posts/", include("feed.posts.urls")),
]
