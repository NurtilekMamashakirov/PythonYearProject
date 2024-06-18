from datetime import datetime

import pytz
import requests

from main import config
from main.models import Link, Chat
from main.utils import link_parser


def notify_bot_about_updates():
    # получаем все ссылки из базы данных
    links = Link.objects.all()
    print(links)
    # обход всех ссылок
    for link in links:
        # если эта ссылка от гх, то ...
        if link_parser.is_github_url(link.url):
            link_to_update = handle_github_updates(link)
            if link_to_update is not None:
                notify_bot(link_to_update)
        # если эта ссылка от stack, то ...
        if link_parser.is_stack_overflow_url(link.url):
            # если по ссылке есть обновление, то функция вернет эту ссылку, если нет, то - None
            link_to_update = handle_stack_overflow_updates(link)
            # если есть обновление, оповещаем об этом бота
            if link_to_update is not None:
                notify_bot(link_to_update)


# функция для обработки ссылки на гх
def handle_github_updates(link):
    # получаем url, с помощью которого будем обращаться к апи гх
    url_to_api = link_parser.get_url_for_github_request(link.url)
    # отправляем get-запрос на гх
    response = requests.get(url_to_api)

    # если запрос успешный, то ...
    if response.status_code == 200:
        # получаем json запроса
        json_response = response.json()
        # если json пуст, то и обнолвения точно нет, следовательно ничего не возвращаем
        if len(json_response) != 0:
            # получаем время последнего обновления (коммит, комментарий, пулл реквест и тд)
            last_activity_time = datetime.strptime(json_response[0]['created_at'], '%Y-%m-%dT%H:%M:%SZ')

            # Имитация логов
            print("Ссылка: ", link.url)
            print("Updated_at: ", link.updated_at)
            print("Last activity time: ", pytz.UTC.localize(last_activity_time), "\n")
            # Имитация логов

            # если время последнего обновления ссылки позже, чем у нас хранится в бд, то сохраняем новое время и возваращем ссылку
            if pytz.UTC.localize(last_activity_time) > link.updated_at:
                print("I am here!! GIT")
                link.updated_at = pytz.UTC.localize(last_activity_time)
                link.save()
                return link


# функция для обработки ссылки на стек
def handle_stack_overflow_updates(link):
    # получаем url, с помощью которого будем обращаться к апи стека
    url_to_api = link_parser.get_url_for_stack_overflow_request(link.url)
    # отправляем get-запрос на стек
    response = requests.get(url_to_api)

    # если запрос успешный, то ...
    if response.status_code == 200:
        # получаем json запроса
        json_response = response.json()
        # получаем список всех ответов
        answers_on_question = json_response['items']
        # если список пуст, то и обнолвения точно нет, следовательно ничего не возвращаем
        if len(answers_on_question) != 0:
            # получаем последний ответ
            last_answer = answers_on_question[0]
            # получаем время последнего ответа
            last_activity_time = datetime.utcfromtimestamp(last_answer['last_activity_date'])

            # Имитация логов
            print("Ссылка: ", link.url)
            print("Updated_at: ", link.updated_at)
            print("Last activity time: ", pytz.UTC.localize(last_activity_time), '\n')
            # Имитация логов

            # если время последнего ответа по ссылке позже, чем у нас хранится в бд, то сохраняем новое время и возваращем ссылку
            if pytz.UTC.localize(last_activity_time) > link.updated_at:
                print("I am here!! STACK")
                link.updated_at = pytz.UTC.localize(last_activity_time)
                link.save()
                return link


# функция для оповещения бота
def notify_bot(link):
    # с помощью этой функции получаем все чаты, которые хранят эту ссылку
    chats_of_link = get_chats_of_link(link)
    # генерируем список id этих чатов
    chat_ids = [chat.id for chat in chats_of_link]
    # готовим словарь, содержащий ссылку и все его чаты, для оповещения бота
    data_of_update = {"url": link.url, "chat_ids": chat_ids}

    # имитация лога
    print(data_of_update)
    # имитация лога

    # отправляем боту информацию об обновленной ссылке и его чатах
    requests.post(config.BOT_URL + config.LINKS_URI_PATH, json=data_of_update)


# функция для получения всех чатов, которые хранят данную в параметры ссылку
def get_chats_of_link(link):
    chats_of_link = []
    chats = Chat.objects.all()
    for chat in chats:
        if link.url in [link_of_chat.url for link_of_chat in chat.links.all()]:
            chats_of_link.append(chat)
    return chats_of_link
