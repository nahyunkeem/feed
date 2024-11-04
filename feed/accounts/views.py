from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer


class SignUpAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=201)

