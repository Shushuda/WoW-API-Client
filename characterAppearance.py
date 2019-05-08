from utils import deep_get


def get_face_type(self):
    return deep_get(self.character_profile, 'appearance', 'faceVariation')


def get_skin_color(self):
    return deep_get(self.character_profile, 'appearance', 'skinColor')


def get_hair_type(self):
    return deep_get(self.character_profile, 'appearance', 'hairVariation')


def get_hair_color(self):
    return deep_get(self.character_profile, 'appearance', 'hairColor')


def get_feature_type(self):
    return deep_get(self.character_profile, 'appearance', 'featureVariation')


def get_show_helm(self):
    return deep_get(self.character_profile, 'appearance', 'showHelm')


def get_show_cloak(self):
    return deep_get(self.character_profile, 'appearance', 'showCloak')
