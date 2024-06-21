import requests
import telebot
from django.core.management.base import BaseCommand

from main import utils
from main.config import SCRAPPER_URL, CHATS_PATH, LINKS_PATH

bot = telebot.TeleBot('6699167118:AAGpFnYx282aZ0FLjzb6VfgFXLYjarw8X28')

help_message = ('Доступны следующие комманды: \n '
                '/start -- запуск бота \n '
                '/help -- информация о командах \n'
                '/track -- начать отслеживать ссылку\n'
                '/untrack -- закончить отслеживание ссылки\n'
                '/list -- список отслеживаемых ссылок ')

unknown_message = 'Команда не распознана'


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        @bot.message_handler()
        def message_handler(message: telebot.types.Message):
            if message.text.lower() == '/start':
                start_handler(message)
            elif message.text.lower() == '/help':
                help_handler(message)
            elif message.text.lower().split(' ')[0] == '/track' and len(message.text.split(' ')) == 2:
                track_handler(message)
            elif message.text.lower().split(' ')[0] == '/untrack' and len(message.text.split(' ')) == 2:
                untrack_handler(message)
            elif message.text.lower() == '/list':
                list_handler(message)
            else:
                bot.send_message(message.chat.id, unknown_message)

        bot.polling(non_stop=True)


# обработка при комманде /start
def start_handler(message: telebot.types.Message):
    chat_id = message.chat.id
    response = requests.get(SCRAPPER_URL + CHATS_PATH)
    # проверка доступности scrapper на данный момент
    if response.status_code == 200:
        chats = response.json()['chats']
        if str(chat_id) in (str(chat['id']) for chat in chats):
            bot.send_message(chat_id, 'Бот уже запущен')
        else:
            bot.send_message(chat_id, f'Добро пожаловать, {message.from_user.first_name}!')
            requests.post(SCRAPPER_URL + CHATS_PATH, data={'chat_id': chat_id})
    else:
        bot.send_message(chat_id, 'Выявлена ошибка. Наша команда разработчиков уже устраняет проблему.')


# обработка при команде /help
def help_handler(message: telebot.types.Message):
    bot.send_message(message.chat.id, help_message)


# обработка при команде /track
def track_handler(message: telebot.types.Message):
    chat_id = message.chat.id
    response = requests.get(SCRAPPER_URL + CHATS_PATH)
    # проверка доступности scrapper на данный момент
    if response.status_code != 200:
        bot.send_message(chat_id, 'Выявлена ошибка. Наша команда разработчиков уже устраняет проблему.')
        return
    # проверка на то, что чат зарегестрирован
    if not (str(chat_id) in (str(chat['id']) for chat in response.json()['chats'])):
        bot.send_message(chat_id, 'Вы не запустили бота. Пожалуйста, пропишите команду /start.')
        return
    link = message.text.split(' ')[1].lower()
    # если эта ссылка от гх или стека, то
    if utils.link_is_available(link):
        # получение всех ссылок чата через scrapper
        response_all_links_of_chat = requests.get(SCRAPPER_URL + LINKS_PATH, params={'chat_id': chat_id})
        if response_all_links_of_chat.status_code == 200:
            all_links_of_chat = response_all_links_of_chat.json()
            if link in (link_of_chat['url'] for link_of_chat in all_links_of_chat):
                bot.send_message(chat_id, 'Данная ссылка уже отслеживается.')
            else:
                response_post_link = requests.post(SCRAPPER_URL + LINKS_PATH, data={'chat_id': chat_id, 'url': link})
                if response_post_link.status_code == 200:
                    bot.send_message(chat_id, f'Ссылка {link} успешно добавлена!')
                else:
                    bot.send_message(chat_id, f'Выявлена ошибка. Наша команда разработчиков уже устраняет проблему.')
        else:
            bot.send_message(chat_id, 'Выявлена ошибка. Наша команда разработчиков уже устраняет проблему.')
    else:
        bot.send_message(chat_id,
                         'Ссылка в неверном формате, либо она неактивна. Это должна быть ссылка на репозиторий в '
                         'github или на вопрос в stack overflow.')


# обработка при команде /untrack
def untrack_handler(message: telebot.types.Message):
    chat_id = message.chat.id
    response = requests.get(SCRAPPER_URL + CHATS_PATH)
    # проверк доступности scrapper на данный момент
    if response.status_code != 200:
        bot.send_message(chat_id, 'Выявлена ошибка. Наша команда разработчиков уже устраняет проблему.')
        return
    # проверка на то, что чат зарегестрирован
    if not (str(chat_id) in (str(chat['id']) for chat in response.json()['chats'])):
        bot.send_message(chat_id, 'Вы не запустили бота. Пожалуйста, пропишите команду /start.')
        return
    link = message.text.split(' ')[1].lower()
    # получение всех ссылок чата через scrapper
    response_all_links_of_chat = requests.get(SCRAPPER_URL + LINKS_PATH, params={'chat_id': chat_id})
    if response_all_links_of_chat.status_code == 200:
        all_links_of_chat = response_all_links_of_chat.json()
        if link in (link_of_chat['url'] for link_of_chat in all_links_of_chat):
            response_delete_link = requests.delete(SCRAPPER_URL + LINKS_PATH, data={'chat_id': chat_id, 'url': link})
            if response_delete_link.status_code == 200:
                bot.send_message(chat_id, f'Ссылка {link} успешно удалена!')
            else:
                bot.send_message(chat_id, 'Выявлена ошибка. Наша команда разработчиков уже устраняет проблему.')
        else:
            bot.send_message(chat_id, 'Данной ссылки нет в вашем списке.')
    else:
        bot.send_message(chat_id, 'Выявлена ошибка. Наша команда разработчиков уже устраняет проблему.')


# обработка при команде /list
def list_handler(message: telebot.types.Message):
    chat_id = message.chat.id
    response = requests.get(SCRAPPER_URL + CHATS_PATH)
    # проверк доступности scrapper на данный момент
    if response.status_code != 200:
        bot.send_message(chat_id, 'Выявлена ошибка. Наша команда разработчиков уже устраняет проблему.')
        return
    # проверка на то, что чат зарегестрирован
    if not (str(chat_id) in (str(chat['id']) for chat in response.json()['chats'])):
        bot.send_message(chat_id, 'Вы не запустили бота. Пожалуйста, пропишите команду /start.')
        return
    # получение всех ссылок чата через scrapper
    response_all_links_of_chat = requests.get(SCRAPPER_URL + LINKS_PATH, params={'chat_id': chat_id})
    if response_all_links_of_chat.status_code == 200:
        all_links_of_chat = response_all_links_of_chat.json()
        if len(all_links_of_chat) > 0:
            list_message_to_user = ''
            count = 1
            for link in all_links_of_chat:
                list_message_to_user += str(count) + '. ' + link['url'] + '\n'
                count += 1
            bot.send_message(chat_id, list_message_to_user)
        else:
            bot.send_message(chat_id,
                             'У вас ещё нет ссылок. Вы можете добавить свою первую ссылку с помощью команды /track.')
    else:
        bot.send_message(chat_id, 'Выявлена ошибка. Наша команда разработчиков уже устраняет проблему.')
