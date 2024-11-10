from django.urls import path, include
from . import views

urlpatterns = [
    path("signup/", views.SignUpAPIView.as_view()),
    path("signin/", views.SigninAPIView.as_view()),
    path("signout/", views.SignoutAPIView.as_view()),
]