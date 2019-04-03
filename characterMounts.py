from utils import deep_get, get_each_from_dict


def get_mount_num_collected(self):
    return deep_get(self.character_profile, 'mounts', 'numCollected')


def get_mount_num_not_collected(self):
    return deep_get(self.character_profile, 'mounts', 'numNotCollected')


def get_mount_collected_spellId(self):
    mounts = deep_get(self.character_profile, 'mounts', 'collected')
    return get_each_from_dict(mounts, 'spellId')
