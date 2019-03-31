import requests
from utils import convert_race_name, convert_faction_name, convert_class_name, convert_gender_name


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
            f'https://{region}.api.blizzard.com/wow/character/{realm}/{character_name}?fields=guild&fields=appearance&fields=achievements&fields=feed&fields=mounts&access_token={access_token}'
        )
        return response

    def get_last_modified(self):
        return self.character_profile_request.headers['last-modified']

    def get_last_modified_timestamp(self):
        return self.character_profile.get('lastModified')

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
        if 'thumbnail' in self.character_profile.keys():
            return f"http://render-{self.region}.worldofwarcraft.com/character/{self.character_profile.get('thumbnail')}"
        else:
            return None

    def get_faction(self):
        return convert_faction_name(self.character_profile.get('faction'))

    def get_total_honorable_kills(self):
        return self.character_profile.get('totalHonorableKills')