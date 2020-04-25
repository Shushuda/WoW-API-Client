import requests
from exceptions import APIConnectionError


def get_realm_list(access_token, region, locale):
    try:
        response = requests.get(
            f'https://{region}.api.blizzard.com/data/wow/realm/index?namespace=dynamic-{region}&locale={locale}&access_token={access_token}'  # noqa
        )
    except requests.exceptions.ConnectionError as e:
        raise APIConnectionError(e)

    if response.status_code == 401:
        e = "Invalid access token"
        raise APIConnectionError(e)

    realm_list = response.json()

    try:
        del realm_list['_links']
    except KeyError:
        pass
    try:
        for realm in realm_list['realms']:
            try:
                del realm['key']
            except KeyError:
                pass
    except KeyError:
        pass

    return realm_list.get('realms')
