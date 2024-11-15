from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, SigninSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


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
        if serializer.update(request.data):
            return Response({"message": "사용자 인증이 완료되었습니다."})


class SigninAPIView(TokenObtainPairView):
    serializer_class = SigninSerializer

