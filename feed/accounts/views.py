from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, SigninSerializer


class SignUpAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "message": "사용자 등록이 완료되었습니다."
            }, status=status.HTTP_201_CREATED)
        
    def patch(self, request):
        serializer = CustomUserSerializer()
        if serializer.auth_validate(request.data):
            return Response({"message": "사용자 인증이 완료되었습니다."})


class SigninAPIView(APIView):
    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        respon = serializer.Signin(request.data)
        if respon:
            return Response(respon)
