import re

import requests
from django.test import TestCase


# Create your tests here.
def link_is_available(link: str):
    pattern_gh = r'^https://github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$'
    match_gh = re.match(pattern_gh, link)

    pattern_sof = r'^https://(ru.)?stackoverflow.com/questions/[0-9]+/[%a-zA-Z0-9_-]+$'
    match_sof = re.match(pattern_sof, link)

    return (bool(match_gh) or bool(match_sof)) and (requests.get(link).status_code == 200)


print(link_is_available(
    "https://ru.stackoverflow.com/questions/511085/%D0%A7%D1%82%D0%BE-%D1%82%D0%B0%D0%BA%D0%BE%D0%B5-null-pointer-exception-%D0%B8-%D0%BA%D0%B0%D0%BA-%D0%B5%D0%B3%D0%BE-%D0%B8%D1%81%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D1%82%D1%8C"))
