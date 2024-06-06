from django.test import TestCase

from main.utils.link_parser import is_stack_overflow_url, get_url_for_stack_overflow_request

# Create your tests here

print(is_stack_overflow_url(
    "https://stackoverflow.com/questions/453161/how-can-i-save-application-settings-in-a-windows-forms-application"))
print(get_url_for_stack_overflow_request(
    "https://stackoverflow.com/questions/453161/how-can-i-save-application-settings-in-a-windows-forms-application"))
