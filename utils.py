def convert_class_name(class_id):
    class_list = {
        1: 'Warrior', 2: 'Paladin', 3: 'Hunter', 4: 'Rogue', 5: 'Priest',
        6: 'Death Knight', 7: 'Shaman', 8: 'Mage', 9: 'Warlock', 10: 'Monk',
        11: 'Druid', 12: 'Demon Hunter', None: 'None',
    }
    return class_list[class_id]


def convert_race_name(race_id):
    race_list = {
        1: 'Human', 2: 'Orc', 3: 'Dwarf', 4: 'Night Elf', 5: 'Undead',
        6: 'Tauren', 7: 'Gnome', 8: 'Troll', 9: 'Goblin', 10: 'Blood Elf',
        11: 'Draenei', 22: 'Worgen', 24: 'Pandaren', 25: 'Pandaren',
        26: 'Pandaren', 27: 'Nightborne', 28: 'Highmountain Tauren',
        29: 'Void Elf', 30: 'Lightforged Draenei', 31: 'Zandalari Troll',
        32: 'Kul Tiran', 34: 'Dark Iron Dwarf', 36: "Mag'har Orc",
        None: 'None',
    }
    return race_list[race_id]


def convert_gender_name(gender_id):
    gender_list = {
        0: 'Male', 1: 'Female', None: 'None',
    }
    return gender_list[gender_id]


def convert_faction_name(faction_id):
    faction_list = {
        0: 'Alliance', 1: 'Horde', 2: 'Neutral', None: 'None',
    }
    return faction_list[faction_id]


def deep_get(dicti, *keys):
    for key in keys:
        try:
            dicti = dicti[key]
        except KeyError:
            return None
    return dicti


def get_character_thumbnail(character_profile, region, img_type):
    end_point = f"http://render-{region}.worldofwarcraft.com/character/"
    if 'thumbnail' in character_profile.keys():
        thumbnail = character_profile.get('thumbnail').replace('avatar',
                                                               img_type)
        return f"{end_point}{thumbnail}"
    else:
        return None


def get_each_from_dict(dicti, *keys):
    i_list = []

    for item in dicti:
        i_list.append(deep_get(item, *keys))

    return i_list


def get_each_item_slot(slots, dicti, *keys):
    i_list = []
    for slot in slots:
        for key in keys:
            i_list.append(deep_get(dicti, 'items', slot, key))

    return i_list


def get_item_icon(img_end_point, size):
    end_point = f"https://wow.zamimg.com/images/wow/icons/{size}/"
    return f"{end_point}{img_end_point}.jpg"


def fix_realm_name(realm):
    return realm.lower().replace(' ', '-')
