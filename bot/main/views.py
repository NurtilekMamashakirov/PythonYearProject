from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.management.commands.bot import bot


# Create your views here.
class LinkUpdatesView(APIView):
    def post(self, request):
        data = request.data
        link = data['url']
        chat_ids = data['chat_ids']
        for chat_id in chat_ids:
            chat_id = int(chat_id)
            bot.send_message(chat_id, f'Обновление по ссылке {link}')
        return Response('', status=status.HTTP_200_OK)
