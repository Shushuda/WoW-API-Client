import requests


class Connect:

    @staticmethod
    def get_token(region, client_id, client_secret):
        data = {'grant_type': 'client_credentials'}

        response = requests.post(
            f'https://{region}.battle.net/oauth/token', data=data, auth=(client_id, client_secret)
        )

        return response.json()['access_token']
