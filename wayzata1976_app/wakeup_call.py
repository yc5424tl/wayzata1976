import os
import requests
import http


if __name__ == "__main__":
 
    send_request()


    def send_request():
        response = requests.get('https://wayzata76.herokuapp.com')
        if response.status_code == http.HTTPStatus.OK:
            print(response)
        else:
            print(response)