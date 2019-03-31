import requests
from utils import convert_race_name, convert_faction_name, convert_class_name, convert_gender_name


class Character:

    # imports of other methods placed in separate files for clarity
    from characterMounts import get_mount_collected_spellId
    from characterMounts import get_mount_num_collected
    from characterMounts import get_mount_num_not_collected
    from characterAchievements import get_completed_achievements
    from characterAppearance import get_character_face_type
    from characterAppearance import get_character_skin_color
    from characterAppearance import get_character_hair_type
    from characterAppearance import get_character_hair_color
    from characterAppearance import get_character_feature_type
    from characterAppearance import get_character_show_helm
    from characterAppearance import get_character_show_cloak

    def __init__(self, access_token, region, realm, character_name):
        self.access_token = access_token
        self.region = region
        self.realm = realm
        self.character_name = character_name

        self.character_profile_request = self.get_character_profile(access_token, region, realm, character_name)
        self.character_profile = self.character_profile_request.json()

    @staticmethod
    def get_character_profile(access_token, region, realm, character_name):
        # TODO
        # make an error class with exception handling (connectionError etc)
        # make the app throw those errors outside of the app for the end-user to handle themselves
        response = requests.get(
            f'https://{region}.api.blizzard.com/wow/character/{realm}/{character_name}?fields=appearance&fields=achievements&fields=feed&fields=mounts&access_token={access_token}'
        )
        return response

    def get_character_last_modified(self):
        return self.character_profile_request.headers['last-modified']

    def get_character_last_modified_timestamp(self):
        return self.character_profile['lastModified']

    def get_character_name(self):
        return self.character_profile['name']

    def get_character_realm(self):
        return self.character_profile['realm']

    def get_character_battlegroup(self):
        return self.character_profile['battlegroup']

    def get_character_class(self):
        return convert_class_name(self.character_profile['class'])

    def get_character_race(self):
        return convert_race_name(self.character_profile['race'])

    def get_character_gender(self):
        return convert_gender_name(self.character_profile['gender'])

    def get_character_level(self):
        return self.character_profile['level']

    def get_character_achievement_points(self):
        return self.character_profile['achievementPoints']

    def get_character_avatar(self):
        return f"http://render-{self.region}.worldofwarcraft.com/character/{self.character_profile['thumbnail']}"

    def get_character_faction(self):
        return convert_faction_name(self.character_profile['faction'])

    def get_total_honorable_kills(self):
        return self.character_profile['totalHonorableKills']