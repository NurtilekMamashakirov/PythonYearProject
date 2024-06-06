from datetime import datetime

import pytz
import requests

from main import config
from main.models import Link, Chat
from main.utils import link_parser


def notify_bot_about_updates():
    links = Link.objects.all()
    for link in links:
        if link_parser.is_github_url(link.url):
            link_to_update = handle_github_updates(link)
            if link_to_update is not None:
                notify_bot(link_to_update)
        if link_parser.is_stack_overflow_url(link.url):
            link_to_update = handle_stack_overflow_updates(link)
            if link_to_update is not None:
                notify_bot(link_to_update)


def handle_github_updates(link):
    url_to_api = link_parser.get_url_for_github_request(link.url)
    response = requests.get(url_to_api)

    if response.status_code == 200:
        json_response = response.json()
        if len(json_response) != 0:
            last_activity_time = datetime.strptime(json_response[0]['created_at'], '%Y-%m-%dT%H:%M:%SZ')

            # Имитация логов
            print("Ссылка: ", link.url)
            print("Updated_at: ", link.updated_at)
            print("Last activity time: ", pytz.UTC.localize(last_activity_time), "\n")
            # Имитация логов

            if pytz.UTC.localize(last_activity_time) > link.updated_at:
                print("I am here!! GIT")
                link.updated_at = pytz.UTC.localize(last_activity_time)
                link.save()
                return link


def handle_stack_overflow_updates(link):
    url_to_api = link_parser.get_url_for_stack_overflow_request(link.url)
    response = requests.get(url_to_api)

    if response.status_code == 200:
        json_response = response.json()
        answers_on_question = json_response['items']
        if len(answers_on_question) != 0:
            last_answer = answers_on_question[0]
            last_activity_time = datetime.utcfromtimestamp(last_answer['last_activity_date'])

            # Имитация логов
            print("Ссылка: ", link.url)
            print("Updated_at: ", link.updated_at)
            print("Last activity time: ", pytz.UTC.localize(last_activity_time), '\n')
            # Имитация логов

            if pytz.UTC.localize(last_activity_time) > link.updated_at:
                print("I am here!! STACK")
                link.updated_at = pytz.UTC.localize(last_activity_time)
                link.save()
                return link


def notify_bot(link):
    chats_of_link = get_chats_of_link(link)
    chat_ids = [chat.id for chat in chats_of_link]
    data_of_update = {"url": link.url, "chat_ids": chat_ids}
    print(data_of_update)
    requests.post(config.BOT_URL + config.LINKS_URI_PATH, json=data_of_update)


def get_chats_of_link(link):
    chats_of_link = []
    chats = Chat.objects.all().values()
    for chat in chats:
        if link.url in [link.url for link in chat.links.values()]:
            chats_of_link.append(chat)
    return chats_of_link
