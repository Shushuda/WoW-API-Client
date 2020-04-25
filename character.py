from datetime import datetime
from typing import Tuple, Any

from utils import get_character_media, fix_realm_name, deep_get, \
    get_each_item_slot, get_each_from_dict, get_endpoint_data, \
    get_character_data, get_character_encounters, get_character_collection, \
    fix_item_media


class Character:

    def __init__(self, access_token, region, realm, character_name):
        self.access_token = access_token
        self.region = region
        self.realm = fix_realm_name(realm)
        self.character_name = character_name.lower()

        self.character_profile, self.character_profile_request = \
            self.get_character_profile(
                self.access_token, self.region, self.realm,
                self.character_name)

    @staticmethod
    def get_character_profile(access_token: object, region: object,
                              realm: object, character_name: object)\
            -> Tuple[dict, Any]:
        main_endpoint = f'https://{region}.api.blizzard.com/profile/wow/character/{realm}/{character_name}?namespace=profile-{region}&locale=en_GB'  # noqa

        character_profile_request = get_endpoint_data(main_endpoint,
                                                      access_token)
        character_data = character_profile_request.json()
        try:
            del character_data['_links']
        except KeyError:
            pass

        data_key_list = ["avatar_url", "bust_url", "render_url"]
        media_data = get_character_media(character_data, access_token, 'media',
                                         data_key_list)
        try:
            character_data['media'].update(media_data)
            del character_data['media']['href']
        except KeyError:
            character_data.update({'media': media_data})

        achievements_key_list = ["total_quantity", "total_points",
                                 "achievements", "category_progress",
                                 "recent_events"]
        achievements_data = get_character_data(character_data, access_token,
                                               'achievements',
                                               achievements_key_list)
        try:
            character_data['achievements'].update(achievements_data)
            del character_data['achievements']['href']
        except KeyError:
            pass

        titles_key_list = ["active_title", "titles"]
        titles_data = get_character_data(character_data, access_token,
                                         'titles', titles_key_list)
        try:
            character_data['titles'].update(titles_data)
            del character_data['titles']['href']
        except KeyError:
            pass

        pvp_key_list = ["honor_level", "pvp_map_statistics", "honorable_kills"]
        pvp_data = get_character_data(character_data, access_token,
                                      'pvp_summary', pvp_key_list)
        try:
            character_data['pvp_summary'].update(pvp_data)
            del character_data['pvp_summary']['href']
        except KeyError:
            pass

        dungeons_data = get_character_encounters(character_data, access_token,
                                                 'dungeons')
        try:
            character_data['encounters'].update(dungeons_data)
        except KeyError:
            pass

        raids_data = get_character_encounters(character_data, access_token,
                                              'raids')
        try:
            character_data['encounters'].update(raids_data)
            del character_data['encounters']['href']
        except KeyError:
            pass

        spec_key_list = ["specializations"]
        spec_data = get_character_data(character_data, access_token,
                                       'specializations', spec_key_list)
        try:
            character_data['specializations'].update(spec_data)
            del character_data['specializations']['href']
        except KeyError:
            pass

        stats_key_list = ["health", "power", "power_type", "speed", "strength",
                          "agility", "intellect", "stamina", "melee_crit",
                          "melee_haste", "mastery", "bonus_armor", "lifesteal",
                          "versatility", "versatility_damage_done_bonus",
                          "versatility_healing_done_bonus",
                          "versatility_damage_taken_bonus", "avoidance",
                          "attack_power", "main_hand_damage_min",
                          "main_hand_damage_max", "main_hand_speed",
                          "main_hand_dps", "off_hand_damage_min",
                          "off_hand_damage_max", "off_hand_speed",
                          "off_hand_dps", "spell_power", "spell_penetration",
                          "spell_crit", "mana_regen", "mana_regen_combat",
                          "armor", "dodge", "parry", "block", "ranged_crit",
                          "ranged_haste", "spell_haste", "corruption"]
        stats_data = get_character_data(character_data, access_token,
                                        'statistics', stats_key_list)
        try:
            character_data['statistics'].update(stats_data)
            del character_data['statistics']['href']
        except KeyError:
            pass

        equipment_key_list = ["equipped_items"]
        equipment_data = get_character_data(character_data, access_token,
                                            'equipment', equipment_key_list)
        equipment_data = fix_item_media(equipment_data, access_token)
        try:
            character_data['equipment'].update(equipment_data)
            del character_data['equipment']['href']
        except KeyError:
            pass

        pets_data = get_character_collection(character_data, access_token,
                                             'pets')
        try:
            character_data['collections'].update(pets_data)
        except KeyError:
            pass

        mounts_data = get_character_collection(character_data, access_token,
                                               'mounts')
        try:
            character_data['collections'].update(mounts_data)
            del character_data['collections']['href']
        except KeyError:
            pass

        rep_key_list = ["reputations"]
        rep_data = get_character_data(character_data, access_token,
                                      'reputations', rep_key_list)
        try:
            character_data['reputations'].update(rep_data)
            del character_data['reputations']['href']
        except KeyError:
            pass

        achievement_stats_key_list = ["categories"]
        achievement_stats_data = get_character_data(character_data,
                                                    access_token,
                                                    'achievements_statistics',
                                                    achievement_stats_key_list)
        try:
            character_data['achievements_statistics'].update(
                achievement_stats_data)
            del character_data['achievements_statistics']['href']
        except KeyError:
            pass

        return character_data, character_profile_request

    def get_id(self):
        return self.character_profile.get('id')

    def get_name(self):
        return self.character_profile.get('name')

    def get_gender(self):
        return deep_get(self.character_profile, 'gender', 'name')

    def get_faction(self):
        return deep_get(self.character_profile, 'faction', 'name')

    def get_race(self):
        return deep_get(self.character_profile, 'race', 'name')

    def get_class(self):
        return deep_get(self.character_profile, 'character_class', 'name')

    def get_active_spec(self):
        return deep_get(self.character_profile, 'active_spec', 'name')

    def get_realm(self):
        return deep_get(self.character_profile, 'realm', 'name')

    def get_realm_slug(self):
        return deep_get(self.character_profile, 'realm', 'slug')

    def get_guild_name(self):
        return deep_get(self.character_profile, 'guild', 'name')

    def get_guild_id(self):
        return deep_get(self.character_profile, 'guild', 'id')

    def get_guild_realm(self):
        return deep_get(self.character_profile, 'guild', 'realm')

    def get_guild_faction(self):
        return deep_get(self.character_profile, 'guild', 'faction')

    def get_level(self):
        return self.character_profile.get('level')

    def get_experience(self):
        return self.character_profile.get('experience')

    def get_achievement_points(self):
        return self.character_profile.get('achievement_points')

    def get_achievements_quantity(self):
        return deep_get(self.character_profile, 'achievements',
                        'total_quantity')

    def get_achievements(self):
        return deep_get(self.character_profile, 'achievements',
                        'achievements')

    def get_achievements_category_progress(self):
        return deep_get(self.character_profile, 'achievements',
                        'category_progress')

    def get_achievements_recent_events(self):
        return deep_get(self.character_profile, 'achievements',
                        'recent_events')

    def get_titles(self):
        return deep_get(self.character_profile, 'titles', 'titles')

    def get_active_title(self):
        return deep_get(self.character_profile, 'titles', 'active_title')

    def get_honor_level(self):
        return deep_get(self.character_profile, 'pvp_summary', 'honor_level')

    def get_pvp_map_statistics(self):
        return deep_get(self.character_profile, 'pvp_summary',
                        'pvp_map_statistics')

    def get_honorable_kills(self):
        return deep_get(self.character_profile, 'pvp_summary',
                        'honorable_kills')

    def get_raid_encounters(self):
        return deep_get(self.character_profile, 'encounters', 'raids')

    def get_dungeon_encounters(self):
        return deep_get(self.character_profile, 'encounters', 'dungeons')

    def get_avatar(self):
        return deep_get(self.character_profile, 'media', 'avatar_url')

    def get_main_picture(self):
        return deep_get(self.character_profile, 'media', 'render_url')

    def get_inset_picture(self):
        return deep_get(self.character_profile, 'media', 'bust_url')

    def get_last_login_timestamp(self):
        time = self.character_profile.get('last_login_timestamp')
        if time is None:
            return None
        else:
            return datetime.fromtimestamp(time // 1000.0)

    def get_avg_ilvl(self):
        return self.character_profile.get('average_item_level')

    def get_avg_ilvl_equipped(self):
        return self.character_profile.get('equipped_item_level')

    def get_specs(self):
        return deep_get(self.character_profile, 'specializations',
                        'specializations')

    def get_statistics(self):
        return self.character_profile.get('statistics')

    def get_items_equipped(self):
        return deep_get(self.character_profile, 'equipment', 'equipped_items')

    def get_items_equipped_id(self):
        item_list = deep_get(self.character_profile, 'equipment',
                             'equipped_items')
        if item_list:
            return get_each_from_dict(item_list, 'item', 'id')
        else:
            return None

    def get_item_slot(self, slot, *item_info_keys):
        item_list = deep_get(self.character_profile, 'equipment',
                             'equipped_items')
        if item_list:
            try:
                item = get_each_item_slot([slot], item_list, *item_info_keys)[slot]
                return item
            except KeyError:
                return None
        else:
            return None

    def get_face_type(self):
        # TODO
        pass

    def get_skin_color(self):
        # TODO
        pass

    def get_hair_type(self):
        # TODO
        pass

    def get_hair_color(self):
        # TODO
        pass

    def get_feature_type(self):
        # TODO
        pass

    def get_mounts(self):
        return deep_get(self.character_profile, 'collections', 'mounts')

    def get_pets(self):
        return deep_get(self.character_profile, 'collections', 'pets')

    def get_mount_num_collected(self):
        mounts = deep_get(self.character_profile, 'collections', 'mounts',
                          'mounts')
        return len(mounts)

    def get_mount_collected_spell_id(self):
        mounts = deep_get(self.character_profile, 'collections', 'mounts',
                          'mounts')
        return get_each_from_dict(mounts, 'mount', 'id')

    def get_reputations(self):
        return deep_get(self.character_profile, 'reputations', 'reputations')

    def get_achievement_statistics(self):
        return deep_get(self.character_profile, 'achievements_statistics',
                        'categories')
