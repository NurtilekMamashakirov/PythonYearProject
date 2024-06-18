from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chat, Link
from .serializers import ChatSerializer, LinkSerializer
from .services import tg_chat_service, link_service


# Create your views here.


class ChatApiView(APIView):
    # обработка get-запросов на api/chats, возваращает все чаты
    def get(self, request):
        chats = Chat.objects.all()
        return Response({"chats": ChatSerializer(chats, many=True).data})

    # обработка post-запроса на api/chats, сохраняет отправленный чат
    def post(self, request):
        new_chat = tg_chat_service.create_chat(request.data["chat_id"])
        return Response(ChatSerializer(new_chat).data)

    # обработка delete-запроса на api/chats, удаляет отправленный чат
    def delete(self, request):
        chat_to_delete = tg_chat_service.delete_chat(request.data["chat_id"])
        return Response(ChatSerializer(chat_to_delete).data)


class LinkApiView(APIView):
    # обработка get-запроса на api/links, возваращет все ссылки чаты, id которого был передан в параметрах
    def get(self, request):
        chat_id = request.query_params.get("chat_id")
        links = link_service.get_links_of_chat(chat_id)
        return Response(LinkSerializer(links, many=True).data)

    # обработка post-запроса на api/links, добавляет ссылку к чату, id которого был отправлен
    def post(self, request):
        chat_id = request.data["chat_id"]
        url = request.data["url"]
        new_link = link_service.create_link(chat_id, url)
        return Response(LinkSerializer(new_link).data)

    # обработка delete-запроса на api/links, удаляет ссылку у чата, id которого был отправлен
    def delete(self, request):
        chat_id = request.data["chat_id"]
        url = request.data["url"]
        link_to_delete = link_service.delete_link(chat_id, url)
        return Response(LinkSerializer(link_to_delete).data)
