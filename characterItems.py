from utils import get_each_item_slot, get_item_icon, deep_get


def get_items_equipped_id(self):
    slots = ['head', 'neck', 'shoulder', 'back', 'chest', 'shirt', 'wrist', 'hands', 'waist', 'legs', 'feet',
             'finger1', 'finger2', 'trinket1', 'trinket2', 'mainHand', 'offHand']
    return get_each_item_slot(slots, self.character_profile, 'id')


def get_item_slot(self, slot):
    item = get_each_item_slot([slot], self.character_profile, 'id', 'name', 'itemLevel', 'icon')
    img_end_point = item[3]
    item.pop(3)
    icons = [get_item_icon(img_end_point, 'small'), get_item_icon(img_end_point, 'medium'),
             get_item_icon(img_end_point, 'large')]
    item.extend(icons)
    return item


def get_avg_ilvl(self):
    return deep_get(self.character_profile, 'items', 'averageItemLevel')


def get_avg_ilvl_equipped(self):
    return deep_get(self.character_profile, 'items', 'averageItemLevelEquipped')
