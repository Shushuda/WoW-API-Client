import requests

from exceptions import APIConnectionError


def deep_get(dicti, *keys):
    for key in keys:
        try:
            dicti = dicti[key]
        except KeyError:
            return None
    return dicti


def get_endpoint_data(endpoint, token):
    try:
        token_url = f"&access_token={token}"
        response = requests.get(f"{endpoint}{token_url}")
    except requests.exceptions.ConnectionError as e:
        raise APIConnectionError(e)

    if response.status_code == 401:
        e = "Invalid access token"
        raise APIConnectionError(e)

    return response


def get_character_media(character_profile, token, data_name, key_list):
    data = get_character_data(character_profile, token, data_name, key_list)
    if data != {}:
        return data
    else:
        fallback_end_point = \
            f"https://render-eu.worldofwarcraft.com/shadow/"
        fallback = "avatar/2-1.jpg"
        return {'avatar_url': f"{fallback_end_point}{fallback}"}


def get_character_data(character_profile, token, data_name, key_list):
    if data_name in character_profile.keys():
        endpoint = deep_get(character_profile, data_name, 'href')
        full_data = get_endpoint_data(endpoint, token).json()
        data = {key: value for key, value in full_data.items()
                if key in key_list}
        return data
    else:
        return {}


def get_character_encounters(character_profile, token, data_name):
    base_key_list = ["dungeons", "raids"]
    base_data = get_character_data(character_profile, token, 'encounters',
                                   base_key_list)
    data = get_character_data(base_data, token, data_name, ['expansions'])
    if data:
        return {data_name: data}
    else:
        return {}


def get_character_collection(character_profile, token, data_name):
    base_key_list = ["pets", "mounts"]
    base_data = get_character_data(character_profile, token, 'collections',
                                   base_key_list)
    data = get_character_data(base_data, token, data_name, data_name)
    if data:
        return {data_name: data}
    else:
        return {}


def get_each_from_dict(dicti, *keys):
    i_list = []

    for item in dicti:
        i_list.append(deep_get(item, *keys))

    return i_list


def get_each_item_slot(slots, dicti, *keys):
    i_dict = {}
    for slot in slots:
        for key in keys:
            i_dict[key] = (deep_get(dicti, 'items', slot, key))

    return i_dict


def get_item_icon(img_end_point, size):
    end_point = f"https://wow.zamimg.com/images/wow/icons/{size}/"
    return f"{end_point}{img_end_point}.jpg"


def fix_realm_name(realm):
    return realm.lower().replace(' ', '-')
