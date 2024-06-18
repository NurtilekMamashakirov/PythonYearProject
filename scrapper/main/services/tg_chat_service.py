from main.models import Chat


# запись чата в бд
def create_chat(id):
    if Chat.objects.filter(id=id).exists():
        return Chat(id=0)
    else:
        return Chat.objects.create(
            id=id
        )


# удаление чата из бд
def delete_chat(id):
    if Chat.objects.filter(id=id).exists():
        Chat.objects.get(id=id).delete()
        return Chat(id=id)
    else:
        return Chat(id=0)
