from main.models import Chat, Link


def get_links_of_chat(chat_id):
    if not Chat.objects.filter(id=chat_id).exists():
        return []
    chat = Chat.objects.get(id=chat_id)
    return chat.links


def create_link(chat_id, url):
    if Chat.objects.filter(id=chat_id).exists():
        link = Link.objects.get_or_create(url=url)
        chat = Chat.objects.get(id=chat_id)
        chat.links.add(link[0])
        chat.save()
        return link[0]
    else:
        return Link(url='')


def delete_link(chat_id, url):
    if Chat.objects.filter(id=chat_id).exists():
        link = Link.objects.get(url=url)
        chat = Chat.objects.get(id=chat_id)
        chat.links.remove(link)
        chat.save()
        return link
    else:
        return Link(url='')
