import re

import requests


def link_is_available(link: str):
    pattern_gh = r'^https://github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$'
    match_gh = re.match(pattern_gh, link)

    pattern_sof = r'^https://(ru.)?stackoverflow.com/questions/[0-9]+/[%a-zA-Z0-9_-]+$'
    match_sof = re.match(pattern_sof, link)

    return (bool(match_gh) or bool(match_sof)) and (requests.get(link).status_code == 200)
