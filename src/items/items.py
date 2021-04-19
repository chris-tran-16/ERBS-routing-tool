from src.util.fetch import DataFetcher
import json
import os


class ItemList:

    def __init__(self):

        self.all_items = None
        self.all_items_by_name = None
        self.spawn_dict = None

    def populate_items(self, data_folder="data/", api_key="", api_key_file=None):

        df = DataFetcher()
        if api_key_file is not None:
            df.read_api_key("real_api_key.txt")
        else:
            df.set_api_key(api_key)

        if not os.path.isfile(f"{data_folder}/english_items.json"):
            df.dump_english_items(folder="data/")

        if not os.path.isfile(f"{data_folder}/armor.json"):
            df.dump_english_items(folder="data/")
        if not os.path.isfile(f"{data_folder}/weapons.json"):
            df.dump_english_items(folder="data/")
        if not os.path.isfile(f"{data_folder}/spawn.json"):
            df.dump_english_items(folder="data/")
        if not os.path.isfile(f"{data_folder}/consumable.json"):
            df.dump_english_items(folder="data/")
        if not os.path.isfile(f"{data_folder}/misc.json"):
            df.dump_english_items(folder="data/")
        if not os.path.isfile(f"{data_folder}/special.json"):
            df.dump_english_items(folder="data/")

        with open("data/english_items.json", "r") as fin:
            english_data = json.load(fin)
        with open("data/armor.json", "r") as fin:
            armor_data = json.load(fin)
        with open("data/weapons.json", "r") as fin:
            weapon_data = json.load(fin)
        with open("data/spawn.json", "r") as fin:
            spawn_data = json.load(fin)
        with open("data/consumable.json", "r") as fin:
            consumable_data = json.load(fin)
        with open("data/misc.json", "r") as fin:
            misc_data = json.load(fin)
        with open("data/special.json", "r") as fin:
            special_data = json.load(fin)

        spawn_dict = dict()
        for spawn_d in spawn_data:
            item_code = spawn_d["itemCode"]
            spawn_dict.setdefault(spawn_d["itemCode"], dict())
            spawn_dict[item_code].setdefault("areaType", []).append(spawn_d["areaType"])
            spawn_dict[item_code].setdefault("areaCode", []).append(spawn_d["areaCode"])
            spawn_dict[item_code].setdefault("dropCount", []).append(spawn_d["dropCount"])

        english_dict = {d["Code"]: d for d in english_data}

        weapon_dict = {d["code"]: Weapon(d) for d in weapon_data}
        armor_dict = {d["code"]: Armor(d) for d in armor_data}
        consumable_dict = {d["code"]: Consumable(d) for d in consumable_data}
        misc_dict = {d["code"]: Misc(d) for d in misc_data}
        special_dict = {d["code"]: Special(d) for d in special_data}

        # process english names
        for weapon in weapon_dict.values():
            weapon.get_english_name(english_dict)
        for armor in armor_dict.values():
            armor.get_english_name(english_dict)
        for consumable in consumable_dict.values():
            consumable.get_english_name(english_dict)
        for misc in misc_dict.values():
            misc.get_english_name(english_dict)
        for special in special_dict.values():
            special.get_english_name(english_dict)

        # process spawning
        for weapon in weapon_dict.values():
            weapon.add_spawn_data(spawn_dict)
        for armor in armor_dict.values():
            armor.add_spawn_data(spawn_dict)
        for misc in misc_dict.values():
            misc.add_spawn_data(spawn_dict)
        for consumable in consumable_dict.values():
            consumable.add_spawn_data(spawn_dict)
        for special in special_dict.values():
            special.add_spawn_data(spawn_dict)

        all_items = {**weapon_dict, **armor_dict, **misc_dict, **consumable_dict, **special_dict}

        # instead, make components list for each uncommon item
        for item_code in all_items:
            all_items[item_code].recursive_item_components(all_items)

        # make consumable and drop items "everywhere"
        # TODO: special items
        all_spawn_areas = set([d["areaType"] for d in spawn_data])
        all_spawn_codes = set([d["areaCode"] for d in spawn_data])
        for item_code in all_items:
            if all_items[item_code].name == "Leather" \
                    or all_items[item_code].name == "Branch" \
                    or all_items[item_code].name == "Stone" \
                    or all_items[item_code].name == "Water":
                all_items[item_code].spawnArea = list(all_spawn_areas)
                # spawn_dict[item_code] = {"areaType": list(all_spawn_areas), "areaCode": list(all_spawn_codes),
                #                          "dropCount": [30] * len(all_spawn_areas)}
                spawn_dict[item_code] = {"areaType": [], "areaCode": [], "dropCount": []}

        self.all_items = all_items
        self.all_items_by_name = {self.all_items[code].name: self.all_items[code] for code in all_items}

        self.spawn_dict = spawn_dict

    def find_item_code_by_name(self, name):
        item = [i for i in self.all_items if self.all_items[i].name == name]
        if len(item) > 1:
            item_code = item[0]
        else:
            item_code = -1

        return item_code


class Item:

    def __init__(self, item_dict=None):
        self.code = ""

        self.makeMaterial1 = -1
        self.makeMaterial2 = -1
        self.consumable = ""

        self.itemType = ""
        self.name = ""
        self.itemGrade = ""

        self.spawnArea = []
        self.spawnAreaCode = []
        self.dropCount = []

        self.common_components = []

        if item_dict is not None:
            self.item_dict = self.from_dict(item_dict)

    def from_dict(self, item_dict):
        pass

    def _from_dict(self, item_dict):
        if item_dict is not None:
            self.code = item_dict["code"]
            self.name = item_dict["name"]
            self.itemType = item_dict["itemType"]
            self.itemGrade = item_dict["itemGrade"]
            self.makeMaterial1 = item_dict["makeMaterial1"]
            self.makeMaterial2 = item_dict["makeMaterial2"]

    def get_english_name(self, english_dict):
        if self.code in english_dict:
            self.name = english_dict[self.code]["Name"]

    def add_spawn_data(self, spawn_dict):
        if self.code in spawn_dict:
            self.spawnArea = spawn_dict[self.code]["areaType"]
            self.spawnAreaCode = spawn_dict[self.code]["areaCode"]
            self.dropCount = spawn_dict[self.code]["dropCount"]

    def recursive_item_components(self, all_items):

        def _recursive_item_components(item):
            if item.itemGrade == "Common" or (item.makeMaterial1 == 0 or item.makeMaterial2 == 0):
                if item.code != self.code:
                    self.common_components.append(item.code)
            else:
                _recursive_item_components(all_items[item.makeMaterial1])
                _recursive_item_components(all_items[item.makeMaterial2])

        _recursive_item_components(all_items[self.code])

    def __str__(self):
        self_str = f"""Item Name: {self.name}
        Item Type: {self.itemType}
        Item Grade: {self.itemGrade}"""
        return self_str


class Weapon(Item):

    def __init__(self, item_dict=None):
        super().__init__(item_dict)

        self.weaponType = ""

        if item_dict is not None:
            self.from_dict(item_dict)

    def from_dict(self, item_dict):
        self._from_dict(item_dict)

        self.weaponType = item_dict["weaponType"]


class Armor(Item):

    def __init__(self, item_dict=None):
        super().__init__(item_dict)
        self.armorType = ""

        if item_dict is not None:
            self.from_dict(item_dict)

    def from_dict(self, item_dict):
        self._from_dict(item_dict)

        self.armorType = item_dict["armorType"]


class Misc(Item):

    def __init__(self, item_dict=None):
        super().__init__(item_dict)

    def from_dict(self, item_dict):
        self._from_dict(item_dict)


class Consumable(Item):

    def __init__(self, item_dict=None):
        super().__init__(item_dict)

    def from_dict(self, item_dict):
        self._from_dict(item_dict)


class Special(Item):

    def __init__(self, item_dict=None):
        super().__init__(item_dict)

    def from_dict(self, item_dict):
        self._from_dict(item_dict)
