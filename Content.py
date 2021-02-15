from abc import ABC
import typing as t
import config

import pandas as pd
import numpy as np


# Mod List

common_mods = "life defense fire cold lightning phys chaos attack caster crit speed influence random".split(" ")

resists = "fire cold lightning".split(" ")

colours = "red green blue white".split(" ")

fractures = "pref1/3 suff1/3 1/5".split(" ")

reforge_methods = "kpref ksuff".split(" ")

basic_format = "```CSS\n" \
               "WTS softcore \n\n" \
               "{method}\n" \
               "```"


basic_price_format = "[{price}]{distance}({amount}x) {mod_name}"
aug_price_format = "[{price}]{distance}({amount}x) Aug / Augment {mod_name}"
remove_price_format = "[{price}]{distance}({amount}x) Rem / Remove {mod_name}"
rem_add_price_format = "[{price}]{distance}({amount}x) Rem/Add {mod_name}"
non_price_format = "[{price}]{distance}({amount}x) Remove Non-{mod_name}, Add {mod_name}"
resist_price_format = "{from_} to {to} ({amount}x)"

class Mod(ABC):

    def __init__(self):
        self.mod_name = None

    def increment(self, method):
        pass

    def decrement(self, method):
        pass


class Common(Mod):

    def __init__(self, mod_name: str = None, prices=None):
        super().__init__()
        self.mod_name = mod_name
        self.price_aug = "offer" if prices is None else prices['aug']
        self.price_remove = "offer" if prices is None else prices['remove']
        self.price_rem_add = "offer" if prices is None else prices['remadd']
        self.price_non = "offer" if prices is None else (prices["non"] if "non" in prices.keys() else "offer")

        self.amount_aug = 0
        self.amount_remove = 0
        self.amount_rem_add = 0
        self.amount_non = 0

    def increment(self, method):
        self._crement(method, increment=True)

    def decrement(self, method):
        self._crement(method, increment=False)

    def _crement(self, method, increment: bool):
        """
        :param method: either aug, remove, rem_add, remadd
        :return: None
        changes amount by 1
        """
        crement = 1 if increment else -1
        if method == "aug":
            self.amount_aug += crement
            self.amount_aug = 0 if self.amount_aug < 0 else self.amount_aug
        elif method == "remove":
            self.amount_remove += crement
            self.amount_remove = 0 if self.amount_remove < 0 else self.amount_remove
        elif method == "rem_add" or method == "remadd":
            self.amount_rem_add += crement
            self.amount_rem_add = 0 if self.amount_rem_add < 0 else self.amount_rem_add
        elif method == "non":
            self.amount_non += crement
            self.amount_non = 0 if self.amount_non < 0 else self.amount_non
        else:
            raise NotImplementedError("method {} could not be found, it should be either aug, remove, rem_add, remadd".format(method))

    def set_amount_to_zero(self, method):
        if method == "aug":
            self.amount_aug = 0
        elif method == "remove":
            self.amount_remove = 0
        elif method == "rem_add" or method == "remadd":
            self.amount_rem_add = 0
        elif method == "non":
            self.amount_non = 0
        else:
            raise NotImplementedError("method {} could not be found, it should be either aug, remove, rem_add, remadd".format(method))


class Reforge(Mod):

    def __init__(self, prices=None):
        super().__init__()

        self.price_kpref = "offer" if prices is None else prices["kpref"]
        self.price_ksuff = "offer" if prices is None else prices["ksuff"]

        self.amount_kpref = 0
        self.amount_ksuff = 0

    def increment(self, method):
        self._crement(method, increment=True)

    def decrement(self, method):
        self._crement(method, increment=False)

    def _crement(self, method, increment: bool):
        crement = 1 if increment else -1

        if method == "kpref":
            self.amount_kpref += crement
            self.amount_kpref = 0 if self.amount_kpref < 0 else self.amount_kpref
        elif method == "ksuff":
            self.amount_ksuff += crement
            self.amount_ksuff = 0 if self.amount_ksuff < 0 else self.amount_ksuff
        else:
            raise NotImplementedError()

    def set_amount_to_zero(self, method):
        if method == "kpref":
            self.amount_kpref = 0
        elif method == "ksuff":
            self.amount_ksuff = 0
        else:
            raise NotImplementedError()


class Resist(Mod):

    def __init__(self, prices=None):
        super().__init__()

        self.amount_resist = pd.DataFrame(np.zeros((3, 3), dtype=np.int))
        self.amount_resist.index = ["fire", "cold", "lightning"]
        self.amount_resist.columns = ["fire", "cold", "lightning"]

        self.price_resist = prices['changeres']

    def increment(self, from_, to):
        self._crement(from_, to, increment=True)

    def decrement(self, from_, to):
        self._crement(from_, to, increment=False)

    def _crement(self, from_, to, increment=True):

        crement = 1 if increment else - 1
        self.amount_resist.loc[from_, to] += crement
        self.amount_resist.loc[from_, to] = 0 if self.amount_resist.loc[from_, to] < 0 else self.amount_resist.loc[from_, to]

    def set_amount_to_zero(self, from_, to):
        self.amount_resist.loc[from_, to] = 0


class Fracture(Mod):
    def __init__(self, prices=None):
        super().__init__()

        self.amount = dict()
        self.amount["pref1/3"] = 0
        self.amount["suff1/3"] = 0
        self.amount["1/5"] = 0

        self.prices = dict()
        self.prices['pref1/3'] = prices['pref1/3']
        self.prices["suff1/3"] = prices["suff1/3"]
        self.prices["1/5"] = prices["1/5"]

    def increment(self, method):
        self._crement(method, increment=True)

    def decrement(self, method):
        self._crement(method, increment=False)

    def _crement(self, method, increment=True):
        crement = 1 if increment else -1
        self.amount[method] += crement
        self.amount[method] = 0 if self.amount[method] < 0 else self.amount[method]

    def set_amount_to_zero(self, method):
        self.amount[method] = 0


class Colour(Mod):

    def __init__(self, prices=None):
        super().__init__()

        self.amount = dict()
        self.prices = dict()

        for colour in colours:
            self.amount[colour] = 0
            self.prices[colour] = prices[colour]

    def increment(self, method):
        self._crement(method, increment=True)

    def decrement(self, method):
        self._crement(method, increment=False)

    def _crement(self, method, increment=True):
        crement = 1 if increment else -1
        self.amount[method] += crement
        self.amount[method] = 0 if self.amount[method] < 0 else self.amount[method]

    def set_amount_to_zero(self, method):
        self.amount[method] = 0


def parse_prices():
    with open(config.prices_path) as f:
        raw = f.read()
    raw = raw.replace("\n", "").replace(" ", "").lower().split(":::")

    raw_dict = dict()
    for mod in raw:
        raw_dict.update(parse_mod_prices_into_dict(mod))

    print(raw_dict)
    return raw_dict


def parse_mod_prices_into_dict(mod_prices):
    mod_prices = mod_prices.split("::")

    if mod_prices[0].lower() in common_mods:
        return {mod_prices[0]: {method.split(":")[0]: method.split(":")[1] for method in mod_prices[1].split(";") if len(method) > 0}}
    elif mod_prices[0].lower() == "reforge":
        return {"reforge": {method.split(":")[0]: method.split(":")[1] for method in mod_prices[1].split(";") if len(method) > 0}}
    elif mod_prices[0].lower() == "fracture":
        return {"fracture": {method.split(":")[0]: method.split(":")[1] for method in mod_prices[1].split(";") if
                            len(method) > 0}}
    elif mod_prices[0].lower() == "changecolour":
        return {"changecolour": {method.split(":")[0]: method.split(":")[1] for method in mod_prices[1].split(";") if
                      len(method) > 0}}
    elif mod_prices[0].lower() == "changeres":
        return {mod_prices[0]: {method.split(":")[0]: method.split(":")[1] for method in mod_prices[1].split(";") if
                                len(method) > 0}}
    else:
        print(mod_prices)
        return {}

def reload():
    global prices, commons, reforge, resist, fracture, change_colour
    prices = parse_prices()
    commons = [Common(mod, prices[mod] if mod in prices.keys() else None) for mod in common_mods]
    reforge = Reforge(prices["reforge"] if "reforge" in prices.keys() else None)
    resist = Resist(prices["changeres"] if "changeres" in prices.keys() else None)
    fracture = Fracture(prices["fracture"] if "fracture" in prices.keys() else None)
    change_colour = Colour(prices["changecolour"] if "changecolour" in prices.keys() else None)

prices = parse_prices()
commons: t.List[Common] = [Common(mod, prices[mod] if mod in prices.keys() else None) for mod in common_mods]
reforge: Reforge = Reforge(prices["reforge"] if "reforge" in prices.keys() else None)
resist: Resist = Resist(prices["changeres"] if "changeres" in prices.keys() else None)
fracture: Fracture = Fracture(prices["fracture"] if "fracture" in prices.keys() else None)
change_colour: Colour = Colour(prices["changecolour"] if "changecolour" in prices.keys() else None)


