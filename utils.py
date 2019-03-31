def convert_class_name(class_id):
    class_list = {
        1: 'Warrior', 2: 'Paladin', 3: 'Hunter', 4: 'Rogue', 5: 'Priest', 6: 'Death Knight', 7: 'Shaman',
        8: 'Mage', 9: 'Warlock', 10: 'Monk', 11: 'Druid', 12: 'Demon Hunter',
    }
    return class_list[class_id]


def convert_race_name(race_id):
    race_list = {
        1: 'Human', 2: 'Orc', 3: 'Dwarf', 4: 'Night Elf', 5: 'Forsaken', 6: 'Tauren',
        7: 'Gnome', 8: 'Troll', 9: 'Goblin', 10: 'Blood Elf', 11: 'Draenei', 22: 'Worgen',
        24: 'Pandaren', 25: 'Pandaren', 26: 'Pandaren', 27: 'Nightborne', 28: 'Highmountain Tauren',
        29: 'Void Elf', 30: 'Lightforged Draenei', 31: 'Zandalari Troll', 32: 'Kul Tiran', 34: 'Dark Iron Dwarf',
        36: "Mag'har Orc",
    }
    return race_list[race_id]


def convert_gender_name(gender_id):
    gender_list = {
        0: 'Male', 1: 'Female',
    }
    return gender_list[gender_id]


def convert_faction_name(faction_id):
    faction_list = {
        0: 'Alliance', 1: 'Horde', 2: 'Neutral',
    }
    return faction_list[faction_id]
