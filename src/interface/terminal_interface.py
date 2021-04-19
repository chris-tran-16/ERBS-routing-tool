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

    def _get_items_in_route(self, route, weapon_type=None, starting_item=None):
        self.routing = Routing(self.item_list, weapon_type=weapon_type)
        self.routing.find_items_in_route(route, starting_item=starting_item)
        self.routing.print_craftable_items()

    def get_input(self):
        pass
