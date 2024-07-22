from rest_framework.response import Response
from rest_framework import status, views

from .middleware import RequestCounterMiddleware


class RequestCounterView(views.APIView):

    def get(self, request) -> Response:
        request_count = RequestCounterMiddleware.get_request_count()
        return Response({"request_count": request_count}, status=status.HTTP_200_OK)


class ResetRequestCounterView(views.APIView):

    def post(self, request) -> Response:
        RequestCounterMiddleware.reset_request_count()
        return Response({'message': 'request count reset successfully'}, status=status.HTTP_204_NO_CONTENT)