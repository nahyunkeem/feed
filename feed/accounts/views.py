from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CustomUserSerializer


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
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)