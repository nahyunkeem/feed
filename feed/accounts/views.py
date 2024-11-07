from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, SigninSerializer


class SignUpAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class SigninAPIView(APIView):
    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        respon = serializer.Signin(request.data)
        if respon:
            return Response(respon, status=status.HTTP_200_OK)