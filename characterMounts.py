from utils import deep_get


def get_mount_num_collected(self):
    return deep_get(self.character_profile, 'mounts', 'numCollected')


def get_mount_num_not_collected(self):
    return deep_get(self.character_profile, 'mounts', 'numNotCollected')


def get_mount_collected_spellId(self):
    mount_list = []
    mounts = deep_get(self.character_profile, 'mounts', 'collected')

    for mount in mounts:
        mount_list.append(mount.get('spellId'))

    return mount_list
