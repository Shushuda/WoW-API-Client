import requests


class Connect:

    @staticmethod
    def get_token(region, client_id, client_secret):
        data = {'grant_type': 'client_credentials'}

        response = requests.post(
            f'https://{region}.battle.net/oauth/token', data=data, auth=(client_id, client_secret)
        )

        return response.json().get('access_token')

    @staticmethod
    # checks whether token is valid, if no then return 0, if yes then return expire time in milliseconds
    def check_token(token, region):
        response = requests.post(
            f'https://{region}.battle.net/oauth/check_token?token={token}'
        )

        if 'error' in response.json().keys():
            return 0
        else:
            return int(response.json().get('exp'))
