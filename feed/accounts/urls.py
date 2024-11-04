from django.urls import path, include
from .views import SignUpAPIView

urlpatterns = [
    path("signup/", SignUpAPIView.as_view()),
]