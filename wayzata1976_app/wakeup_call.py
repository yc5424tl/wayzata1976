import os
import requests
import http


if __name__ == "__main__":
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wayzata76_django.settings")
    # import django

    # django.setup()
    # from wayzata76_agent_

    # function()
    # response = requests.get('url')


    def send_request(url):
        response = requests.get('https://wayzata76.herokuapp.com')
        if response.status_code == http.HTTPStatus.OK:
            pass
        else:
            pass