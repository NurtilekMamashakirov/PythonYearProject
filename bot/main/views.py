from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class LinkUpdatesView(APIView):
    def post(self, request):
        data = request.data
        link = data['link']
        chat_ids = data['chat_ids']
        #todo
        return Response('', status=status.HTTP_200_OK)
