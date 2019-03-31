from utils import deep_get


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
