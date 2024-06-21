from urllib.parse import urlparse

from main import config


# проверяет, является ли url ссылкой на гх
def is_github_url(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname.lower() == config.GITHUB_HOST:
        return True
    else:
        return False


# проверяет, является ли url ссылкой на стек
def is_stack_overflow_url(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname.lower() in config.STACK_OVERFLOW_HOSTS:
        return True
    else:
        return False


# возвращает url для обращения к гх апи
def get_url_for_github_request(url):
    parsed_url = urlparse(url)
    profile_name = parsed_url.path.split('/')[1]
    repos_name = parsed_url.path.split('/')[2]
    return config.GITHUB_API_URL + '/' + profile_name + '/' + repos_name + '/events'

# возвращает url для обращения к стек апи
def get_url_for_stack_overflow_request(url):
    parsed_url = urlparse(url)
    question_id = parsed_url.path.split('/')[2]
    if parsed_url.hostname == config.STACK_OVERFLOW_HOSTS[0]:
        return (config.STACK_OVERFLOW_API_URL + '/questions/' +
                question_id + '/answers?site=stackoverflow&sort=activity')
    if parsed_url.hostname == config.STACK_OVERFLOW_HOSTS[1]:
        return (config.STACK_OVERFLOW_API_URL + '/questions/' +
                question_id + '/answers?site=ru.stackoverflow&sort=activity')
