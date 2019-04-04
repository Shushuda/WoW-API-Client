from datetime import datetime
import requests
from utils import convert_race_name, convert_faction_name, convert_class_name, convert_gender_name, \
    get_character_thumbnail, fix_realm_name
from exceptions import APIConnectionError


class Character:

    # imports of other methods placed in separate files for clarity
    from characterMounts import get_mount_collected_spellId
    from characterMounts import get_mount_num_collected
    from characterMounts import get_mount_num_not_collected
    from characterAchievements import get_completed_achievements
    from characterAppearance import get_face_type
    from characterAppearance import get_skin_color
    from characterAppearance import get_hair_type
    from characterAppearance import get_hair_color
    from characterAppearance import get_feature_type
    from characterAppearance import get_show_helm
    from characterAppearance import get_show_cloak
    from characterGuild import get_guild_name
    from characterFeed import get_feed_dict
    from characterItems import get_items_equipped_id
    from characterItems import get_item_slot
    from characterItems import get_avg_ilvl
    from characterItems import get_avg_ilvl_equipped

    def __init__(self, access_token, region, realm, character_name):
        self.access_token = access_token
        self.region = region
        self.realm = fix_realm_name(realm)
        self.character_name = character_name

        self.character_profile_request = self.get_character_profile(self.access_token, self.region, self.realm,
                                                                    self.character_name)
        self.character_profile = self.character_profile_request.json()

    @staticmethod
    def get_character_profile(access_token, region, realm, character_name):
        try:
            response = requests.get(
                f'https://{region}.api.blizzard.com/wow/character/{realm}/{character_name}?fields=items%2C%20guild%2C%20appearance%2C%20achievements%2C%20feed%2C%20mounts&access_token={access_token}'
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
        return get_character_thumbnail(self.character_profile, self.region, 'avatar')

    def get_main_picture(self):
        return get_character_thumbnail(self.character_profile, self.region, 'main')

    def get_inset_picture(self):
        return get_character_thumbnail(self.character_profile, self.region, 'inset')

    def get_faction(self):
        return convert_faction_name(self.character_profile.get('faction'))

    def get_total_honorable_kills(self):
        return self.character_profile.get('totalHonorableKills')