
def get_deck_of(typ):
    if typ in [2, 3, 4, 12]:
        return 1
    return 0

def print_index(lst: list):
    for i in range(len(lst)):
        print("{} - {}".format(i, lst[i]))


typ = [
    "Normal Monster",
    "Effect Monster",
    "Fusion Monster",
    "Synchro Monster",
    "Xyz Monster",

    "Spell",
    "Quick Spell",
    "Continuous Spell",
    "Field Spell",
    "Equip Spell",

    "Trap",
    "Continuous Trap",

    "Link Monster"
]
