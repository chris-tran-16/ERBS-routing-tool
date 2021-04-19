import os
import errno

sort_dictionary = {
    "Common": 0,
    "Uncommon": 1,
    "Rare": 2,
    "Epic": 3,
    "Legend": 4,
}


def sort_item_list(item_list):
    return sorted(item_list, key=lambda x: (sort_dictionary[x.itemGrade], x.name))


def return_names_from_list(item_list):
    return [i.name for i in item_list]


def check_dir(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
