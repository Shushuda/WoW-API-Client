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
    def api_call():
        try:
            token_url = f"&access_token={token}"
            response = requests.get(f"{endpoint}{token_url}")
            return response
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError(e)
    for retry in range(0, 3):
        result = api_call()
        if result.status_code != 503:
            break

    if result.status_code == 401:
        e = "Invalid access token"
        raise APIConnectionError(e)

    return result


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


def get_each_item_slot(slots, item_list, *keys):
    if not keys:
        keys = ['item', 'slot', 'context', 'bonus_list', 'quality', 'name',
                'azerite_details', 'media', 'item_class', 'item_subclass',
                'inventory_type', 'binding', 'armor', 'stats', 'requirements',
                'level', 'transmog', 'durability']
    i_dict = {}
    for slot in slots:
        for item in item_list:
            if item['slot']['type'] == slot.upper():
                item_data = {key: value for key, value in item.items()
                             if key in keys}
                i_dict.update({slot: item_data})
                break

    return i_dict


def fix_realm_name(realm):
    return realm.lower().replace(' ', '-')


def fix_item_media(equipment_data, access_token):
    try:
        for item in equipment_data['equipped_items']:
            try:
                del item['item']['key']
            except KeyError:
                pass
            try:
                del item['item_class']['key']
            except KeyError:
                pass
            try:
                del item['item_subclass']['key']
            except KeyError:
                pass
            try:
                transmog_endpoint = item['transmog']['item']['key']['href']
                del item['transmog']['item']['key']
                transmog_media_endpoint = get_endpoint_data(
                    transmog_endpoint,
                    access_token).json()['media']['key']['href']
                transmog_data = get_endpoint_data(
                    transmog_media_endpoint, access_token).json()['assets']
                item_icon = [asset['value'] for asset in transmog_data
                             if asset['key'] == 'icon']
                item['transmog'].update({'icon': item_icon})
            except KeyError:
                pass
            try:
                media_endpoint = item['media']['key']['href']
                del item['media']['key']
                item_data = get_endpoint_data(
                    media_endpoint, access_token).json()['assets']
                item_icon = [asset['value'] for asset in item_data
                             if asset['key'] == 'icon']
                item['media'].update({'icon': item_icon})
            except KeyError:
                item.update({'media': None})
    except KeyError:
        pass

    return equipment_data
