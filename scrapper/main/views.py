from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chat, Link
from .serializers import ChatSerializer, LinkSerializer
from .services import tg_chat_service, link_service


# Create your views here.


class ChatApiView(APIView):
    def get(self, request):
        chats = Chat.objects.all()
        return Response({"chats": ChatSerializer(chats, many=True).data})

    def post(self, request):
        # serializer = ChatSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        new_chat = tg_chat_service.create_chat(request.data["chat_id"])
        return Response(ChatSerializer(new_chat).data)

    def delete(self, request):
        # serializer = ChatSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        chat_to_delete = tg_chat_service.delete_chat(request.data["chat_id"])
        return Response(ChatSerializer(chat_to_delete).data)


class LinkApiView(APIView):
    def get(self, request):
        chat_id = request.query_params.get("chat_id")
        links = link_service.get_links_of_chat(chat_id)
        return Response(LinkSerializer(links, many=True).data)

    def post(self, request):
        # serializer = LinkSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        chat_id = request.data["chat_id"]
        url = request.data["url"]
        new_link = link_service.create_link(chat_id, url)
        return Response(LinkSerializer(new_link).data)

    def delete(self, request):
        chat_id = request.data["chat_id"]
        url = request.data["url"]
        link_to_delete = link_service.delete_link(chat_id, url)
        return Response(LinkSerializer(link_to_delete).data)
