from urllib.parse import urlparse


# Create your tests here
def is_stack_overflow_url(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname.lower() in ('stackoverflow.com', 'ru.stackoverflow.com'):
        return True
    else:
        return False


def get_url_for_stack_overflow_request(url):
    parsed_url = urlparse(url)
    question_id = parsed_url.path.split('/')[2]
    if parsed_url.hostname == 'stackoverflow.com':
        return ('https://api.stackexchange.com/2.3' + '/questions/' +
                question_id + '/answers?site=stackoverflow&sort=activity')
    if parsed_url.hostname == 'ru.stackoverflow.com':
        return ('https://api.stackexchange.com/2.3' + '/questions/' +
                question_id + '/answers?site=ru.stackoverflow&sort=activity')


print(is_stack_overflow_url(
    "https://stackoverflow.com/questions/78598763/вопрос-для-теста-telebota-на-python"))
print(get_url_for_stack_overflow_request(
    "https://stackoverflow.com/questions/78598763/вопрос-для-теста-telebota-на-python"))
