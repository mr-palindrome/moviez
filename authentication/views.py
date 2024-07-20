from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterUserSerializer, LoginUserSerializer


class AuthUserView(APIView):

    register_serializer_class = RegisterUserSerializer
    login_serializer_class = LoginUserSerializer
    is_register = None

    def post(self, request):
        if self.is_register:
            serializer = self.register_serializer_class(data=request.data)
        else:
            serializer = self.login_serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):

            response = {
                "access": serializer.validated_data.get("access"),
            }
            status_code = status.HTTP_201_CREATED if self.is_register else status.HTTP_200_OK
            return Response(response, status=status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)