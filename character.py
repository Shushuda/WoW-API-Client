from datetime import datetime
import requests
from utils import convert_race_name, convert_faction_name, \
    convert_class_name, convert_gender_name, get_character_thumbnail, \
    fix_realm_name, deep_get, get_each_item_slot, get_item_icon, \
    get_each_from_dict
from exceptions import APIConnectionError


class Character:

    def __init__(self, access_token, region, realm, character_name):
        self.access_token = access_token
        self.region = region
        self.realm = fix_realm_name(realm)
        self.character_name = character_name

        self.character_profile_request = self.get_character_profile(
            self.access_token, self.region, self.realm, self.character_name)
        self.character_profile = self.character_profile_request.json()

    @staticmethod
    def get_character_profile(access_token: object, region: object,
                              realm: object, character_name: object) -> object:
        try:
            response = requests.get(
                f'https://{region}.api.blizzard.com/wow/character/{realm}/{character_name}?fields=items%2C%20guild%2C%20appearance%2C%20achievements%2C%20feed%2C%20mounts&access_token={access_token}'  # noqa
            )
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError(e)

        if response.status_code == 401:
            e = "Invalid access token"
            raise APIConnectionError(e)

        return response

    def get_last_modified_string(self):
        return self.character_profile_request.headers['last-modified']

    def get_last_modified_timestamp(self):
        time = self.character_profile.get('lastModified')
        if time is None:
            return None
        else:
            return datetime.fromtimestamp(time//1000.0)

    def get_name(self):
        return self.character_profile.get('name')

    def get_realm(self):
        return self.character_profile.get('realm')

    def get_battlegroup(self):
        return self.character_profile.get('battlegroup')

    def get_class(self):
        return convert_class_name(self.character_profile.get('class'))

    def get_race(self):
        return convert_race_name(self.character_profile.get('race'))

    def get_gender(self):
        return convert_gender_name(self.character_profile.get('gender'))

    def get_level(self):
        return self.character_profile.get('level')

    def get_achievement_points(self):
        return self.character_profile.get('achievementPoints')

    def get_avatar(self):
        return get_character_thumbnail(self.character_profile, self.region,
                                       'avatar')

    def get_main_picture(self):
        return get_character_thumbnail(self.character_profile, self.region,
                                       'main')

    def get_inset_picture(self):
        return get_character_thumbnail(self.character_profile, self.region,
                                       'inset')

    def get_faction(self):
        return convert_faction_name(self.character_profile.get('faction'))

    def get_total_honorable_kills(self):
        return self.character_profile.get('totalHonorableKills')

    def get_completed_achievements(self):
        return deep_get(self.character_profile, 'achievements',
                        'achievementsCompleted')

    def get_face_type(self):
        return deep_get(self.character_profile, 'appearance', 'faceVariation')

    def get_skin_color(self):
        return deep_get(self.character_profile, 'appearance', 'skinColor')

    def get_hair_type(self):
        return deep_get(self.character_profile, 'appearance', 'hairVariation')

    def get_hair_color(self):
        return deep_get(self.character_profile, 'appearance', 'hairColor')

    def get_feature_type(self):
        return deep_get(self.character_profile, 'appearance',
                        'featureVariation')

    def get_show_helm(self):
        return deep_get(self.character_profile, 'appearance', 'showHelm')

    def get_show_cloak(self):
        return deep_get(self.character_profile, 'appearance', 'showCloak')

    # VERY big dictionary with various feed data
    # left intact for the end-user to split and use as they please
    def get_feed_dict(self):
        return self.character_profile.get('feed')

    def get_guild_name(self):
        return deep_get(self.character_profile, 'guild', 'name')

    def get_guild_realm(self):
        return deep_get(self.character_profile, 'guild', 'realm')

    def get_guild_members(self):
        return deep_get(self.character_profile, 'guild', 'members')

    def get_guild_achievement_points(self):
        return deep_get(self.character_profile, 'guild', 'achievementPoints')

    def get_guild_emblem_dict(self):
        return deep_get(self.character_profile, 'guild', 'emblem')

    def get_items_equipped_id(self):
        slots = ['head', 'neck', 'shoulder', 'back', 'chest', 'shirt', 'wrist',
                 'hands', 'waist', 'legs', 'feet', 'finger1', 'finger2',
                 'trinket1', 'trinket2', 'mainHand', 'offHand']
        return get_each_item_slot(slots, self.character_profile, 'id')

    def get_item_slot(self, slot):
        item = get_each_item_slot([slot], self.character_profile, 'id', 'name',
                                  'itemLevel', 'icon')
        img_end_point = item['icon']
        del item['icon']
        item['icon_small'] = get_item_icon(img_end_point, 'small')
        item['icon_medium'] = get_item_icon(img_end_point, 'medium')
        item['icon_large'] = get_item_icon(img_end_point, 'large')
        return item

    def get_avg_ilvl(self):
        return deep_get(self.character_profile, 'items', 'averageItemLevel')

    def get_avg_ilvl_equipped(self):
        return deep_get(self.character_profile, 'items',
                        'averageItemLevelEquipped')

    def get_mount_num_collected(self):
        return deep_get(self.character_profile, 'mounts', 'numCollected')

    def get_mount_num_not_collected(self):
        return deep_get(self.character_profile, 'mounts', 'numNotCollected')

    def get_mount_collected_spellId(self):
        mounts = deep_get(self.character_profile, 'mounts', 'collected')
        return get_each_from_dict(mounts, 'spellId')
