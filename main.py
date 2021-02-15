import typing as t
import os

import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk
import numpy as np

import Content
import config


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.commons: t.Union[t.List[CommonCraftElement], None] = None
        self.reforge = None
        self.resist = None
        self.fracture = None
        self.colour = None

        self.common_manager = tk.Frame(self, highlightbackground="black", highlightthickness=1)
        self.common_manager.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.other_manager = tk.Frame(self, highlightbackground="black", highlightthickness=1)
        self.other_manager.grid(row=1, column=0, padx=10, sticky="new")

        self.create_crafts()

        self.textbox_manager = tk.Frame(self)
        self.textbox_manager.grid(row=0, column=1, rowspan=2, padx=10, pady=10, columnspan=3)

        self.clipboard_image = None
        self.aug_text_label = None
        self.aug_textbox = None
        self.aug_clipboard_button = None
        self.remove_text_label = None
        self.remove_textbox = None
        self.remove_clipboard_button = None
        self.rem_add_text_label = None
        self.rem_add_textbox = None
        self.rem_add_clipboard_button = None
        self.other_text_label = None
        self.other_textbox = None
        self.other_clipboard_button = None

        self.create_textboxes()

        self.generation_button = tk.Button(self, text="Generate Copy Pasta", command=self.generate_copy_pasta)
        self.generation_button.grid(row=2, column=1, sticky="NE", padx=10, pady=10)

        self.open_prices = tk.Button(self, text="€", command=self.open_prices, width=4)
        self.open_prices.grid(row=2, column=2, sticky="NE", padx=10, pady=10)

    def create_crafts(self):

        self.commons = [CommonCraftElement(self.common_manager, mod) for mod in Content.commons]

        self.reforge: ReforgeElement = ReforgeElement(self.other_manager, Content.reforge)
        self.fracture: FractureElement = FractureElement(self.other_manager, Content.fracture)
        self.resist: ResistElement = ResistElement(self.other_manager, Content.resist)
        self.colour: ColourElement = ColourElement(self.other_manager, Content.change_colour)

    def create_textboxes(self):

        clipboard = Image.open(config.clipboard_image_path)
        clipboard.thumbnail((30, 30), Image.ANTIALIAS)
        self.clipboard_image = ImageTk.PhotoImage(clipboard)

        self.aug_text_label = tk.Label(self.textbox_manager, text="Augment Copy Pasta:")
        self.aug_text_label.grid(row=0, column=0)
        self.aug_textbox: tk.Text = tk.Text(self.textbox_manager,  width=40, height=6)
        self.aug_textbox.grid(row=1, column=0)
        self.aug_clipboard_button = tk.Button(self.textbox_manager, image=self.clipboard_image, command=lambda: self.copy_to_clipboard(self.aug_textbox))
        self.aug_clipboard_button.grid(row=1, column=1, padx=4, sticky="nw")

        self.remove_text_label = tk.Label(self.textbox_manager, text="Remove Copy Pasta:")
        self.remove_text_label.grid(row=2, column=0)
        self.remove_textbox = tk.Text(self.textbox_manager,  width=40, height=6)
        self.remove_textbox.grid(row=3, column=0)
        self.remove_clipboard_button = tk.Button(self.textbox_manager, image=self.clipboard_image, command=lambda: self.copy_to_clipboard(self.remove_textbox))
        self.remove_clipboard_button.grid(row=3, column=1, padx=4, sticky="nw")

        self.rem_add_text_label = tk.Label(self.textbox_manager, text="Remove+Add Copy Pasta:")
        self.rem_add_text_label.grid(row=4, column=0)
        self.rem_add_textbox = tk.Text(self.textbox_manager,  width=40, height=6)
        self.rem_add_textbox.grid(row=5, column=0)
        self.rem_add_clipboard_button = tk.Button(self.textbox_manager, image=self.clipboard_image, command=lambda: self.copy_to_clipboard(self.rem_add_textbox))
        self.rem_add_clipboard_button.grid(row=5, column=1, padx=4, sticky="nw")

        self.other_text_label = tk.Label(self.textbox_manager, text="Other Copy Pasta:")
        self.other_text_label.grid(row=6, column=0)
        self.other_textbox = tk.Text(self.textbox_manager,  width=40, height=9)
        self.other_textbox.grid(row=7, column=0)
        self.other_clipboard_button = tk.Button(self.textbox_manager, image=self.clipboard_image, command=lambda: self.copy_to_clipboard(self.other_textbox))
        self.other_clipboard_button.grid(row=7, column=1, padx=4, sticky="nw")



    def copy_to_clipboard(self, textbox: tk.Text):

        self.master.clipboard_clear()
        self.master.clipboard_append(textbox.get("1.0", "end"))

    def open_prices(self):
        self.master.withdraw()
        os.system("prices.txt")
        self.master.deiconify()
        Content.reload()

        self.reforge.reforge.price_kpref = Content.reforge.price_kpref
        self.reforge.reforge.price_ksuff = Content.reforge.price_ksuff

        self.colour.colour.prices = Content.change_colour.prices

        self.fracture.fracture.prices = Content.fracture.prices
        for ui, content_craft in zip(self.commons, Content.commons):
            ui.craft.price_non = content_craft.price_non
            ui.craft.price_aug = content_craft.price_aug
            ui.craft.price_remove = content_craft.price_remove
            ui.craft.price_rem_add = content_craft.price_rem_add

        self.resist.resist.price_resist = Content.resist.price_resist
        self.generate_copy_pasta()

    def generate_copy_pasta(self):
        self._generate_augment_copy_pasta()
        self._generate_remove_copy_pasta()
        self._generate_rem_add_copy_pasta()
        self._generate_other_copy_pasta()

    def _generate_augment_copy_pasta(self):

        text = Content.basic_format
        text = text.format(method=config.aug_method_text)

        at_least_1_craft = False
        for craft_element in self.commons:
            if craft_element.craft.amount_aug > 0:
                at_least_1_craft = True
                insert = Content.aug_price_format.format(mod_name=config.mod_copy_pasta_replacement[craft_element.craft.mod_name],
                                                           amount=craft_element.craft.amount_aug,
                                                           distance=" " * (config.price_amount_distance - len(craft_element.craft.price_aug)),
                                                           price=craft_element.craft.price_aug)
                text= text.format(insert + "\n{}")

        self.aug_textbox.delete("1.0", "end")
        self.aug_textbox.insert("1.0", text.format("") if at_least_1_craft else "")

    def _generate_remove_copy_pasta(self):

        text = Content.basic_format
        text = text.format(method=config.remove_method_text)

        at_least_1_craft = False
        for craft_element in self.commons:
            if craft_element.craft.amount_remove > 0:
                at_least_1_craft = True
                insert = Content.remove_price_format.format(mod_name=config.mod_copy_pasta_replacement[craft_element.craft.mod_name],
                                                           amount=craft_element.craft.amount_remove,
                                                           distance=" " * (config.price_amount_distance - len(craft_element.craft.price_remove)),
                                                           price=craft_element.craft.price_remove)
                text = text.format(insert + "\n{}")

        self.remove_textbox.delete("1.0", "end")
        self.remove_textbox.insert("1.0", text.format("") if at_least_1_craft else "")

    def _generate_rem_add_copy_pasta(self):
        text = Content.basic_format
        text = text.format(method=config.rem_add_method_text)

        at_least_1_craft = False
        for craft_element in self.commons:
            if craft_element.craft.amount_rem_add > 0:
                at_least_1_craft = True
                insert = Content.rem_add_price_format.format(mod_name=config.mod_copy_pasta_replacement[craft_element.craft.mod_name],
                                                           amount=craft_element.craft.amount_rem_add,
                                                           price=craft_element.craft.price_rem_add,
                                                           distance=" " * (config.price_amount_distance - len(craft_element.craft.price_rem_add))
                                                           )
                text = text.format(insert + "\n{}")

        self.rem_add_textbox.delete("1.0", "end")
        self.rem_add_textbox.insert("1.0", text.format("") if at_least_1_craft else "")

    def _generate_other_copy_pasta(self):

        text = Content.basic_format
        text = text.format(method="{}")

        at_least_1_craft = False

        for craft_element in self.commons:
            if craft_element.craft.amount_non > 0:
                at_least_1_craft = True
                insert = Content.non_price_format.format(mod_name=config.mod_copy_pasta_replacement[craft_element.craft.mod_name],
                                                           amount=craft_element.craft.amount_non,
                                                           distance=" " * (config.price_amount_distance - len(craft_element.craft.price_non)),
                                                           price=craft_element.craft.price_non)
                text = text.format(insert + "\n{}")

        text = text.format("\n{}")

        if self.reforge.reforge.amount_kpref > 0:
            at_least_1_craft = True
            insert = Content.basic_price_format.format(mod_name=config.mod_copy_pasta_replacement["kpref"],
                                                       amount=self.reforge.reforge.amount_kpref,
                                                       price=self.reforge.reforge.price_kpref,
                                                       distance=" " * (config.price_amount_distance - len(self.reforge.reforge.price_kpref)))
            text = text.format(insert + "\n{}")

        if self.reforge.reforge.amount_ksuff > 0:
            at_least_1_craft = True
            insert = Content.basic_price_format.format(mod_name=config.mod_copy_pasta_replacement["ksuff"],
                                                       amount=self.reforge.reforge.amount_ksuff,
                                                       price=self.reforge.reforge.price_ksuff,
                                                       distance=" " * (config.price_amount_distance - len(self.reforge.reforge.price_ksuff)))
            text = text.format(insert + "\n{}")

        if at_least_1_craft:
            text = text.format("\n{}")

        for method in Content.fractures:
            if self.fracture.fracture.amount[method] > 0:
                at_least_1_craft = True
                insert = Content.basic_price_format.format(mod_name=config.mod_copy_pasta_replacement[method],
                                                       amount=self.fracture.fracture.amount[method],
                                                       price=self.fracture.fracture.prices[method],
                                                       distance=" " * (config.price_amount_distance - len(self.fracture.fracture.prices[method])))
                text = text.format(insert + "\n{}")

        if at_least_1_craft:
            text = text.format("\n{}")

        change_res_text = "Change Resist [{price}]:".format(price=self.resist.resist.price_resist) + "\n{}"
        at_least_1_res = False
        for from_ in ['fire', 'cold', 'lightning']:
            for to in ['fire', 'cold', 'lightning']:
                if self.resist.resist.amount_resist.loc[from_, to] > 0:
                    insert = Content.resist_price_format.format(from_=config.mod_copy_pasta_replacement[from_],
                                                                to=config.mod_copy_pasta_replacement[to],
                                                                amount=self.resist.resist.amount_resist.loc[from_, to])
                    at_least_1_res = True
                    at_least_1_craft = True
                    change_res_text = change_res_text.format(insert + "\n{}")

        change_colour_text = "Change Colour: \n{}"
        at_least_1_colour = False
        for colour_ in Content.colours:
            if self.colour.colour.amount[colour_] > 0:
                at_least_1_craft = True
                at_least_1_colour = True
                insert = Content.basic_price_format.format(mod_name=config.mod_copy_pasta_replacement[colour_],
                                                       amount=self.colour.colour.amount[colour_],
                                                       price=self.colour.colour.prices[colour_],
                                                       distance=" " * (config.price_amount_distance - len(self.colour.colour.prices[colour_])))
                change_colour_text = change_colour_text.format(insert + "\n{}")

        if at_least_1_res:
            text = text.format(change_res_text).format("\n{}")
        if at_least_1_colour:
            text = text.format(change_colour_text)
        self.other_textbox.delete("1.0", "end")
        self.other_textbox.insert("1.0", text.format("") if at_least_1_craft else "")


class CommonCraftElement(tk.Frame):

    def __init__(self, master=None, craft=None):
        super().__init__(master)
        self.master = master

        self.text = "Default Text"

        self.aug_image = None
        self.remove_image = None
        self.rem_add_image = None
        self.non_image = None

        self.aug_button = None
        self.remove_button = None
        self.rem_add_button = None
        self.non_button = None

        self.pack()
        self.craft: Content.Common = craft
        self.create_craft_UI()




    def create_craft_UI(self):

        if self.craft is not None:
            self.text = tk.Label(self, text=self.craft.mod_name.capitalize(), width=10, compound="left")
            self.text.grid(row=0, column=0)

            aug_image = Image.open(config.ex_image_path)
            aug_image.thumbnail((20, 20), Image.ANTIALIAS)
            self.aug_image = ImageTk.PhotoImage(aug_image)
            self.aug_button = tk.Button(self, text=self.craft.amount_aug, image=self.aug_image, height=20, width=30, compound="left")
            self.aug_button.grid(row=0, column=1)
            self.aug_button.bind("<Button-1>", lambda event: self.increment("aug"))
            self.aug_button.bind("<Button-3>", lambda event: self.decrement("aug"))
            self.aug_button.bind("<Shift-Button-1>", lambda event: self.set_amount_to_zero("aug"))

            remove_image = Image.open(config.annul_image_path)
            remove_image.thumbnail((20, 20), Image.ANTIALIAS)
            self.remove_image = ImageTk.PhotoImage(remove_image)
            self.remove_button = tk.Button(self, text=self.craft.amount_remove, image=self.remove_image, height=20, width=30, compound="left")
            self.remove_button.grid(row=0, column=2)
            self.remove_button.bind("<Button-1>", lambda event: self.increment("remove"))
            self.remove_button.bind("<Button-3>", lambda event: self.decrement("remove"))
            self.remove_button.bind("<Shift-Button-1>", lambda event: self.set_amount_to_zero("remove"))

            rem_add_image = Image.open(config.annulex_image_path)
            rem_add_image.thumbnail((20, 20), Image.ANTIALIAS)
            self.rem_add_image = ImageTk.PhotoImage(rem_add_image)
            self.rem_add_button = tk.Button(self, text=self.craft.amount_rem_add, image=self.rem_add_image, height=20, width=30, compound="left")
            self.rem_add_button.grid(row=0, column=3)
            self.rem_add_button.bind("<Button-1>", lambda event: self.increment("remadd"))
            self.rem_add_button.bind("<Button-3>", lambda event: self.decrement("remadd"))
            self.rem_add_button.bind("<Shift-Button-1>", lambda event: self.set_amount_to_zero("remadd"))

            non_image = Image.open(config.redannulex_image_path)
            non_image.thumbnail((20, 20), Image.ANTIALIAS)
            self.non_image = ImageTk.PhotoImage(non_image)
            self.non_button = tk.Button(self, text=self.craft.amount_non, image=self.non_image, height=20, width=30, compound="left")
            self.non_button.grid(row=0, column=4)
            self.non_button.bind("<Button-1>", lambda event: self.increment("non"))
            self.non_button.bind("<Button-3>", lambda event: self.decrement("non"))
            self.non_button.bind("<Shift-Button-1>", lambda event: self.set_amount_to_zero("non"))



    def increment(self, method):
        self.craft.increment(method)
        self.update()

    def decrement(self, method):
        self.craft.decrement(method)
        self.update()

    def set_amount_to_zero(self, method):
        self.craft.set_amount_to_zero(method)
        self.update()


    def update(self):
        self.aug_button.config(text=self.craft.amount_aug)
        if self.craft.amount_aug > 0:
            self.aug_button.config(bg="green")
        else:
            self.aug_button.config(bg="SystemButtonFace")

        self.remove_button.config(text=self.craft.amount_remove)
        if self.craft.amount_remove > 0:
            self.remove_button.config(bg="green")
        else:
            self.remove_button.config(bg="SystemButtonFace")

        self.rem_add_button.config(text=self.craft.amount_rem_add)
        if self.craft.amount_rem_add > 0:
            self.rem_add_button.config(bg="green")
        else:
            self.rem_add_button.config(bg="SystemButtonFace")

        self.non_button.config(text=self.craft.amount_non)
        if self.craft.amount_non > 0:
            self.non_button.config(bg="green")
        else:
            self.non_button.config(bg="SystemButtonFace")


class ReforgeElement(tk.Frame):

    def __init__(self, master=None, reforge: Content.Reforge=None):
        super().__init__(master)
        self.reforge: Content.reforge = reforge

        self.label = tk.Label(self, text="Reforge", width=10)
        self.kpref_button = tk.Button(self, text="K.Pref: {}".format(self.reforge.amount_kpref))
        self.kpref_button.bind("<Button-1>", lambda event: self.increment("kpref"))
        self.kpref_button.bind("<Button-3>", lambda event: self.decrement("kpref"))
        self.kpref_button.bind("<Shift-Button-1>", lambda event: self.set_amount_to_zero("kpref"))

        self.ksuff_button = tk.Button(self, text="K.Suff: {}".format(self.reforge.amount_ksuff))
        self.ksuff_button.bind("<Button-1>", lambda event: self.increment("ksuff"))
        self.ksuff_button.bind("<Button-3>", lambda event: self.decrement("ksuff"))
        self.ksuff_button.bind("<Shift-Button-1>", lambda event: self.set_amount_to_zero("ksuff"))

        self.label.grid(row=0, column=0, sticky="NSEW")
        self.kpref_button.grid(row=0, column=1, sticky="NSEW")
        self.ksuff_button.grid(row=0, column=2, sticky="NSEW")

        self.pack(expand=True, fill="x")

    def increment(self, method):
        self.reforge.increment(method)
        self.update()

    def decrement(self, method):
        self.reforge.decrement(method)
        self.update()

    def set_amount_to_zero(self, method):
        self.reforge.set_amount_to_zero(method)
        self.update()

    def update(self):

        self.kpref_button.config(text="K.Pref: {}".format(self.reforge.amount_kpref))
        if self.reforge.amount_kpref > 0:
            self.kpref_button.config(bg="green")
        else:
            self.kpref_button.config(bg="SystemButtonFace")

        self.ksuff_button.config(text="K.Suff: {}".format(self.reforge.amount_ksuff))
        if self.reforge.amount_ksuff > 0:
            self.ksuff_button.config(bg="green")
        else:
            self.ksuff_button.config(bg="SystemButtonFace")



class ResistElement(tk.Frame):

    def __init__(self, master=None, resist: Content.Resist=None):
        super().__init__(master, highlightbackground="black", highlightthickness=1)
        self.resist = resist
        self.resist_buttons = None
        self.master = master

        self.tranform_image = None
        self.transform_label = None
        self.fire_image = None
        self.fire_label_horizontal = None
        self.fire_label_vertical = None
        self.cold_image = None
        self.cold_label_horizontal = None
        self.cold_label_vertical = None
        self.lightning_image = None
        self.lightning_label_horizontal = None
        self.lightning_label_vertical = None

        self.create_labels()
        self.create_buttons()

        self.pack(side="left", pady=(10, 0))

    def create_labels(self):
        tmp: Image.Image = Image.open(config.resist_transform_image_path)
        tmp.thumbnail((20, 20), Image.ANTIALIAS)
        self.tranform_image = ImageTk.PhotoImage(tmp)
        self.transform_label = tk.Label(self, image=self.tranform_image)
        self.transform_label.grid(row=0, column=0)

        tmp: Image.Image = Image.open(config.fire_image_path)
        tmp.thumbnail((20, 20), Image.ANTIALIAS)
        self.fire_image = ImageTk.PhotoImage(tmp)
        self.fire_label_horizontal = tk.Label(self, image=self.fire_image)
        self.fire_label_vertical = tk.Label(self, image=self.fire_image)
        self.fire_label_horizontal.grid(row=1, column=0)
        self.fire_label_vertical.grid(row=0, column=1)

        tmp: Image.Image = Image.open(config.cold_image_path)
        tmp.thumbnail((20, 20), Image.ANTIALIAS)
        self.cold_image = ImageTk.PhotoImage(tmp)
        self.cold_label_horizontal = tk.Label(self, image=self.cold_image)
        self.cold_label_vertical = tk.Label(self, image=self.cold_image)
        self.cold_label_horizontal.grid(row=2, column=0)
        self.cold_label_vertical.grid(row=0, column=2)

        tmp: Image.Image = Image.open(config.lightning_image_path)
        tmp.thumbnail((20, 20), Image.ANTIALIAS)
        self.lightning_image = ImageTk.PhotoImage(tmp)
        self.lightning_label_horizontal = tk.Label(self, image=self.lightning_image)
        self.lightning_label_vertical = tk.Label(self, image=self.lightning_image)
        self.lightning_label_horizontal.grid(row=3, column=0)
        self.lightning_label_vertical.grid(row=0, column=3)


    def create_buttons(self):

        self.resist_buttons = pd.DataFrame(np.zeros((3, 3)))
        self.resist_buttons.columns = ['fire', 'cold', 'lightning']
        self.resist_buttons.index = ['fire', 'cold', 'lightning']

        for from_ in ['fire', 'cold', 'lightning']:
            for to in [x for x in ['fire', 'cold', 'lightning'] if x != from_]:
                self.resist_buttons.loc[from_, to] = self.create_button(from_, to)

    def create_button(self, from_, to):

        grid_matching = {'fire': 1, 'cold': 2, 'lightning': 3}
        button = tk.Button(self, text=self.resist.amount_resist.loc[from_, to])
        button.bind("<Button-1>", lambda event: self.increment(from_, to))
        button.bind("<Button-3>", lambda event: self.decrement(from_, to))
        button.bind("<Shift-Button-1>", lambda event: self.set_amount_to_zero(from_, to))
        button.grid(row=grid_matching[from_], column=grid_matching[to], sticky="NSEW")
        return button

    def increment(self, from_, to):
        self.resist.increment(from_, to)
        self.update()

    def decrement(self, from_, to):
        self.resist.decrement(from_, to)
        self.update()

    def set_amount_to_zero(self, from_, to):
        self.resist.set_amount_to_zero(from_, to)
        self.update()

    def update(self):
        for from_ in ['fire', 'cold', 'lightning']:
            for to in [x for x in ['fire', 'cold', 'lightning'] if x != from_]:
                self.resist_buttons.loc[from_, to].config(text=self.resist.amount_resist.loc[from_, to])

                if self.resist.amount_resist.loc[from_, to] > 0:
                    self.resist_buttons.loc[from_, to].config(bg="green")
                else:
                    self.resist_buttons.loc[from_, to].config(bg="SystemButtonFace")


class FractureElement(tk.Frame):

    def __init__(self, master=None, fracture: Content.Fracture=None):

        super().__init__(master)
        self.master = master
        self.fracture = fracture

        self.button_replacements = {
            "pref1/3": "P1/3",
            "suff1/3": "S1/3",
            "1/5": "1/5"
        }

        self.buttons = dict()
        self.buttons["pref1/3"] = self.create_button(method="pref1/3", grid_column=1)
        self.buttons["suff1/3"] = self.create_button(method="suff1/3", grid_column=2)
        self.buttons["1/5"] = self.create_button(method="1/5", grid_column=3)

        self.label = tk.Label(self, text="Fracture")
        self.label.grid(row=0, column=0)
        self.pack()

    def create_button(self, method, grid_column: int):
        button = tk.Button(self, text=self.button_replacements[method] + ": " + str(self.fracture.amount[method]))
        button.bind("<Button-1>", lambda event: self.increment(method))
        button.bind("<Button-3>", lambda event: self.decrement(method))
        button.bind("<Shift-Button-1>", lambda event: self.set_amount_to_zero(method))
        button.grid(row=0, column=grid_column, sticky="NSEW")
        return button

    def increment(self, method):
        self.fracture.increment(method)
        self.update()

    def decrement(self, method):
        self.fracture.decrement(method)
        self.update()

    def set_amount_to_zero(self, method):
        self.fracture.set_amount_to_zero(method)
        self.update()

    def update(self):
        for method in Content.fractures:
            self.buttons[method].config(text=self.button_replacements[method] + ": " + str(self.fracture.amount[method]))
            if self.fracture.amount[method] > 0:
                self.buttons[method].config(bg="green")
            else:
                self.buttons[method].config(bg="SystemButtonFace")


class ColourElement(tk.Frame):

    def __init__(self, master, colour):
        super().__init__(master)
        self.master = master
        self.colour = colour

        self.colour_images = dict()
        self.buttons = dict()
        self.buttons["red"] = self.create_button("red", grid_row=0)
        self.buttons["blue"] = self.create_button("blue", grid_row=1)
        self.buttons["green"] = self.create_button("green", grid_row=2)
        self.buttons["white"] = self.create_button("white", grid_row=3)
        self.pack(expand=True, pady=(10, 0))

    def create_button(self, method, grid_row: int):
        tmp = Image.open(config.colour_image_path[method])
        tmp.thumbnail((40, 20), Image.ANTIALIAS)
        self.colour_images[method] = ImageTk.PhotoImage(tmp)

        button = tk.Button(self, image=self.colour_images[method], text=str(self.colour.amount[method]), compound="left")
        button.bind("<Button-1>", lambda event: self.increment(method))
        button.bind("<Button-3>", lambda event: self.decrement(method))
        button.bind("<Shift-Button-1>", lambda event: self.set_amount_to_zero(method))
        button.grid(row=grid_row, column=0, sticky="NSEW")
        return button

    def increment(self, method):
        self.colour.increment(method)
        self.update()

    def decrement(self, method):
        self.colour.decrement(method)
        self.update()

    def set_amount_to_zero(self, method):
        self.colour.set_amount_to_zero(method)
        self.update()

    def update(self):
        for method in Content.colours:
            self.buttons[method].config(text=self.colour.amount[method])
            if self.colour.amount[method] > 0:
                self.buttons[method].config(bg="green")
            else:
                self.buttons[method].config(bg="SystemButtonFace")



if __name__ == "__main__":
    root = tk.Tk()
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    root.iconphoto(False, tk.PhotoImage(file=config.window_icon_path))
    root.title(config.app_title)

    app = Application(master=root)
    app.mainloop()
