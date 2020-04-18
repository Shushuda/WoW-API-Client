from datetime import datetime
from utils import get_character_media, fix_realm_name, deep_get, \
    get_each_item_slot, get_item_icon, get_each_from_dict, get_endpoint_data, \
    get_character_data, get_character_encounters, get_character_collection


class Character:

    def __init__(self, access_token, region, realm, character_name):
        self.access_token = access_token
        self.region = region
        self.realm = fix_realm_name(realm)
        self.character_name = character_name.lower()

        self.character_profile = self.get_character_profile(
            self.access_token, self.region, self.realm, self.character_name)

    @staticmethod
    def get_character_profile(access_token: object, region: object,
                              realm: object, character_name: object) -> dict:
        main_endpoint = f'https://{region}.api.blizzard.com/profile/wow/character/{realm}/{character_name}?namespace=profile-{region}&locale=en_GB'  # noqa

        character_data = get_endpoint_data(main_endpoint, access_token).json()

        data_key_list = ["avatar_url", "bust_url", "render_url"]
        media_data = get_character_media(character_data, access_token, 'media',
                                         data_key_list)
        try:
            character_data['media'].update(media_data)
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
        except KeyError:
            pass

        titles_key_list = ["active_title", "titles"]
        titles_data = get_character_data(character_data, access_token,
                                         'titles', titles_key_list)
        try:
            character_data['titles'].update(titles_data)
        except KeyError:
            pass

        pvp_key_list = ["honor_level", "pvp_map_statistics", "honorable_kills"]
        pvp_data = get_character_data(character_data, access_token,
                                      'pvp_summary', pvp_key_list)
        try:
            character_data['pvp_summary'].update(pvp_data)
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
        except KeyError:
            pass

        spec_key_list = ["specializations"]
        spec_data = get_character_data(character_data, access_token,
                                       'specializations', spec_key_list)
        try:
            character_data['specializations'].update(spec_data)
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
        except KeyError:
            pass

        mythic_key_list = ["current_period"]
        mythic_data = get_character_data(character_data, access_token,
                                         'mythic_keystone_profile',
                                         mythic_key_list)
        try:
            character_data['mythic_keystone_profile'].update(mythic_data)
        except KeyError:
            pass

        equipment_key_list = ["equipped_items"]
        equipment_data = get_character_data(character_data, access_token,
                                            'equipment', equipment_key_list)
        try:
            character_data['equipment'].update(equipment_data)
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
        except KeyError:
            pass

        rep_key_list = ["reputations"]
        rep_data = get_character_data(character_data, access_token,
                                      'reputations', rep_key_list)
        try:
            character_data['reputations'].update(rep_data)
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
        except KeyError:
            pass

        return character_data

    def get_id(self):
        return self.character_profile.get('id')

    def get_name(self):
        return self.character_profile.get('name')

    def get_gender(self):
        return self.character_profile.get('gender')

    def get_faction(self):
        return self.character_profile.get('faction')

    def get_race(self):
        return self.character_profile.get('race')

    def get_class(self):
        return self.character_profile.get('character_class')

    def get_active_spec(self):
        return self.character_profile.get('active_spec')

    def get_realm(self):
        return self.character_profile.get('realm')

    def get_guild_name(self):
        return deep_get(self.character_profile, 'guild', 'name')

    def get_guild_id(self):
        return deep_get(self.character_profile, 'guild', 'id')

    def get_guild_realm(self):
        return deep_get(self.character_profile, 'guild', 'realm')

    def get_guild_fraction(self):
        return deep_get(self.character_profile, 'guild', 'fraction')

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

    def get_pvp_summary(self):
        # TODO
        pass

    def get_raid_encounters(self):
        # TODO
        pass

    def get_dungeon_encounters(self):
        # TODO
        pass

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
        # TODO
        pass

    def get_statistics(self):
        # TODO
        pass

    def get_mythic_keystone_profile(self):
        # TODO
        pass

    def get_items_equipped_id(self):
        # TODO
        pass
        # slots = ['head', 'neck', 'shoulder', 'back', 'chest', 'shirt',
        #          'wrist', 'hands', 'waist', 'legs', 'feet', 'finger1',
        #          'finger2', 'trinket1', 'trinket2', 'mainHand', 'offHand']
        # return get_each_item_slot(slots, self.character_profile, 'id')

    def get_item_slot(self, slot):
        # TODO
        pass
        # item = get_each_item_slot([slot], self.character_profile, 'id',
        #                           'name', 'itemLevel', 'icon')
        # img_end_point = item['icon']
        # del item['icon']
        # item['icon_small'] = get_item_icon(img_end_point, 'small')
        # item['icon_medium'] = get_item_icon(img_end_point, 'medium')
        # item['icon_large'] = get_item_icon(img_end_point, 'large')
        # return item

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

    def get_total_honorable_kills(self):
        # TODO
        pass

    def get_mount_num_collected(self):
        # TODO
        pass

    def get_mount_collected_spell_id(self):
        # TODO
        pass
        # mounts = deep_get(self.character_profile, 'mounts', 'collected')
        # return get_each_from_dict(mounts, 'spellId')

    def get_reputations(self):
        # TODO
        pass

    def get_achievement_statistics(self):
        # TODO
        pass
