import requests
from exceptions import APIConnectionError


class Connect:

    @staticmethod
    def get_token(region, client_id, client_secret):
        data = {'grant_type': 'client_credentials'}

        try:
            response = requests.post(
                f'https://{region}.battle.net/oauth/token', data=data, auth=(client_id, client_secret)
            )
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError(e)

        if 'error' in response.json():
            e = "Bad credentials"
            raise APIConnectionError(e)

        return response.json().get('access_token')

    @staticmethod
    # returns expire time, 0 = expired/invalid
    def check_token(region, token):
        try:
            response = requests.post(
                f'https://{region}.battle.net/oauth/check_token?token={token}'
            )
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError(e)

        if 'error' in response.json().keys():
            return 0
        else:
            return int(response.json().get('exp'))
