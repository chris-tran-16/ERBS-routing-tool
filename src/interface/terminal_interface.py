from src.items.items import *
from src.routing.routing import *
from src.util.fetch import *
from src.util.util import *
import pickle as pkl


class TerminalInterface:

    def __init__(self, data_folder="data/", repopulate=False, api_key="", api_key_file=None):
        self.repopulate = repopulate

        file_name = f"{data_folder}/item_list.pkl"
        if not os.path.isfile(f"{data_folder}/item_list.pkl") or self.repopulate:
            item_list = ItemList()
            item_list.populate_items(data_folder=data_folder, api_key=api_key, api_key_file=api_key_file)

            check_dir(file_name)
            with open(file_name, "wb") as file:
                pkl.dump(item_list, file)
        else:
            with open(file_name, "rb") as file:
                item_list = pkl.load(file)

        self.item_list = item_list

        self.routing = None

        self.options = [
            'Alley',
            'Archery',
            'Avenue',
            'Beach',
            'Cemetery',
            'Church',
            'Dock',
            'Factory',
            'Forest',
            'Hospital',
            'Hotel',
            'Pond',
            'School',
            'Temple',
            'Uptown'
        ]

        self.current_options = self.options.copy()

        self.current_route = []

        self.levels_menu = {
            # 0: {
            #     0: ["Simple", "Currency Conversion", "Items", "Active"] + self.extra_options
            # },
            # 1: {
            #     0: ["Chaos", "Splinters", "Exalt"] + self.level_1_options + self.simple_options + self.extra_options,
            #     1: ["Chaos -> Exalt (buy with Chaos, sell for Exalts)",
            #         "Exalt -> Chaos (buy with Exalt, sell for Chaos)"] + self.level_1_options + self.extra_options,
            #     2: list(price_check.flip_checker.list_types.values()) + self.extra_options,
            #     3: ["Chaos", "Exalt"] + self.extra_options,
            # },
        }

    def _get_items_in_route(self, route, weapon_type=None, starting_item=None):
        self.routing = Routing(self.item_list, weapon_type=weapon_type)
        self.routing.find_items_in_route(route, starting_item=starting_item)
        self.routing.print_craftable_items()

    def _print_options(self):
        print(f"Current route: {self.current_route}")
        print(f"0) Find items")
        for i in range(len(self.current_options)):
            print(f"{i + 1}) {self.current_options[i]}")
        print(f"{len(self.current_options) + 1}) Reset")
        print(f"{len(self.current_options) + 2}) Exit")

    def _update_options(self):
        pass
        # self.levels_menu = {
        #     0: {
        #         0: ["Simple", "Currency Conversion", "Items", "Active"] + self.extra_options
        #     },
        #     1: {
        #         0: ["Chaos", "Splinters", "Exalt"] + self.level_1_options + self.simple_options + self.extra_options,
        #         1: ["Chaos -> Exalt (buy with Chaos, sell for Exalts)",
        #             "Exalt -> Chaos (buy with Exalt, sell for Chaos)"] + self.level_1_options + self.extra_options,
        #         2: list(price_check.flip_checker.list_types.values()) + self.extra_options,
        #         3: ["Chaos", "Exalt"] + self.extra_options,
        #     },
        # }

    def get_input(self):
        self._print_options()
        user_input = int(input("Enter a number: "))
        print()
        if user_input in range(1, len(self.current_options) + 1):
            selected = self.current_options[user_input - 1]
            self.current_route.append(selected)
            self.current_options.remove(selected)
        elif user_input == len(self.current_options) + 1:
            self.current_options = self.options.copy()
            self.current_route = []
        elif user_input == len(self.current_options) + 2:
            exit()
        elif user_input == 0:
            self.routing = Routing(self.item_list, weapon_type="Pistol")
            self.routing.find_items_in_route(self.current_route)
            self.routing.print_craftable_items()
        else:
            print("Invalid input!")
