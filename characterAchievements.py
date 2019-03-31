from utils import deep_get


def get_completed_achievements(self):
    return deep_get(self.character_profile, 'achievements', 'achievementsCompleted')
