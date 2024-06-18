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
    "https://stackoverflow.com/questions/78598763/%d0%92%d0%be%d0%bf%d1%80%d0%be%d1%81-%d0%b4%d0%bb%d1%8f-%d1%82%d0%b5%d1%81%d1%82%d0%b0-telebota-%d0%bd%d0%b0-python"))
