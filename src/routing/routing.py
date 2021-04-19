from src.items.items import ItemList
import itertools
from src.util.util import sort_item_list


def remove_supersets(valid_areas_sets):
    valid_sets = sorted(valid_areas_sets, key=len, reverse=True).copy()

    subsets = []
    while valid_sets:
        cur = valid_sets.pop()
        subsets.append(cur)
        valid_sets = [x for x in valid_sets if not cur <= x]

    return subsets


class Routing:

    def __init__(self, item_list: ItemList, weapon_type=None):
        self.item_list = item_list

        self.weapon_type = weapon_type

        self.items_can_complete = []
        self.weapons_can_complete = []
        self.head_can_complete = []
        self.chest_can_complete = []
        self.arm_can_complete = []
        self.leg_can_complete = []
        self.accessory_can_complete = []

        self.starting_item_type_code = {
            "Pistol": ("Walther PPK", item_list.find_item_code_by_name("Walther PPK"))
        }

    def find_items_in_route(self, route: list, starting_item=None):
        all_items = self.item_list.all_items

        all_items_in_route = [[all_items[i] for i in all_items if location in all_items[i].spawnArea] for location in
                              route]
        all_items_in_route = list(itertools.chain.from_iterable(all_items_in_route))
        all_item_codes_in_route = [item.code for item in all_items_in_route]

        if starting_item:
            all_item_codes_in_route = all_item_codes_in_route + [starting_item]
        items_can_complete = []
        for item_code in all_items:
            if set(all_items[item_code].common_components).issubset(all_item_codes_in_route) and len(
                    all_items[item_code].common_components) > 1:
                items_can_complete.append(all_items[item_code])

        self.items_can_complete = items_can_complete

        weapons_can_complete = [i for i in items_can_complete if i.itemType == "Weapon"]
        if self.weapon_type is not None:
            if isinstance(self.weapon_type, str):
                weapons_can_complete = [i for i in weapons_can_complete if i.weaponType == self.weapon_type]
            elif isinstance(self.weapon_type, list):
                weapons_can_complete = [i for i in weapons_can_complete if i.weaponType in self.weapon_type]
        self.weapons_can_complete = sort_item_list(weapons_can_complete)

        self.head_can_complete = sort_item_list(
            [i for i in items_can_complete if i.itemType == "Armor" and i.armorType == "Head"])
        self.chest_can_complete = sort_item_list(
            [i for i in items_can_complete if i.itemType == "Armor" and i.armorType == "Chest"])
        self.arm_can_complete = sort_item_list(
            [i for i in items_can_complete if i.itemType == "Armor" and i.armorType == "Arm"])
        self.leg_can_complete = sort_item_list(
            [i for i in items_can_complete if i.itemType == "Armor" and i.armorType == "Leg"])
        self.accessory_can_complete = sort_item_list(
            [i for i in items_can_complete if i.itemType == "Armor" and i.armorType == "Trinket"])

    def _print_items(self, item_type, item_list):
        print_str = f"{item_type}: "
        for i in item_list:
            print_str = f"{print_str}{i.name}, "
        print_str = print_str.strip(" ")
        print_str = print_str.rstrip(',')
        return print_str

    def print_craftable_items(self):

        print(self._print_items("Weapons", self.weapons_can_complete))

        print(self._print_items("Head", self.head_can_complete))

        print(self._print_items("Chest", self.chest_can_complete))

        print(self._print_items("Arm", self.arm_can_complete))

        print(self._print_items("Legs", self.leg_can_complete))

        print(self._print_items("Accessory", self.accessory_can_complete))

    def check_if_valid_route(self, route, components_needed):
        for component in components_needed:
            component_spawn_areas = self.item_list.all_items[component].spawnArea
            component_in_route = any([i in route for i in component_spawn_areas])

            if not component_in_route:
                return False

        return True

    def find_potential_areas(self, weapon, head, chest, arm, leg, accessory, other=None, starting_item=None):

        item_list = self.item_list
        all_items_by_name = self.item_list.all_items_by_name
        all_items = self.item_list.all_items

        items_to_make = [weapon, head, chest, arm, leg, accessory]
        if other:
            if isinstance(other, str):
                items_to_make = items_to_make + [other]
            elif isinstance(other, list):
                items_to_make = items_to_make + other

        components_needed = [
            self.item_list.all_items_by_name[item].common_components for item in items_to_make
        ]
        components_needed = list(itertools.chain.from_iterable(components_needed))
        if starting_item:
            if all_items_by_name[starting_item].code in components_needed:
                components_needed.remove(all_items_by_name[starting_item].code)
        components_needed = set(components_needed)

        potential_areas = [
            item_list.spawn_dict[i]["areaType"] for i in components_needed
            if len(item_list.spawn_dict[i]["areaType"]) > 0
        ]
        potential_areas_set = set(itertools.chain.from_iterable(potential_areas))
        combinations_potential_areas = list(
            itertools.combinations(potential_areas_set, 3)) + list(
            itertools.combinations(potential_areas_set, 4)) + list(
            itertools.combinations(potential_areas_set, 5)) + list(
            itertools.combinations(potential_areas_set, 6))

        valid_areas_sets = [i for i in combinations_potential_areas if self.check_if_valid_route(i, components_needed)]
        valid_area_min_sets = remove_supersets(valid_areas_sets)

        return valid_area_min_sets
