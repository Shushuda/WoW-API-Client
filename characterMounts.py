def get_mount_num_collected(self):
    return self.character_profile['mounts']['numCollected']


def get_mount_num_not_collected(self):
    return self.character_profile['mounts']['numNotCollected']


def get_mount_collected_spellId(self):
    mount_list = []
    mounts = self.character_profile['mounts']['collected']

    for item in mounts:
        mount_list.append(item['spellId'])

    return mount_list
