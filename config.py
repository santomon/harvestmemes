import os

prices_path = "prices.txt"
basic_format_path = "basic_format.txt"


clipboard_image_path = os.path.join("assets", "clipboard.png")
annul_image_path = os.path.join("assets", "annul.png")
ex_image_path = os.path.join("assets", "ex.png")
annulex_image_path = os.path.join( "assets", "annulex.png")
redannulex_image_path = os.path.join("assets", "redannulex.png")
window_icon_path = os.path.join("assets", "blue_seed.png")

colour_image_path = {
    "red": os.path.join("assets", "red.png"),
    "blue": os.path.join("assets", "blue.png"),
    "green": os.path.join("assets", "green.png"),
    "white": os.path.join("assets", "white.png")
}


common_image_root_dir = "assets"
common_image_names = {
    "life": "life.png",
    "defense": "es.png",
    "attack": "empty.png",
    "caster": "empty.png",

    "fire": "diy_flame.png",
    "cold": "snowflake.png",
    "lightning": "lightning_bolt.png",
    "phys": "empty.png",
    "chaos": "chaos.png",

    "crit": "ie.png",
    "speed": "speed.png",
    "influence": "shaper.png",
    "random": "dice.png",
}

common_group_lines = [1, 6, 8, 10, 11]

resist_transform_image_path = os.path.join("assets", "arrow_curved.png")
fire_image_path = os.path.join("assets", "diy_flame.png")
cold_image_path = os.path.join("assets", "snowflake.png")
lightning_image_path = os.path.join("assets", "lightning_bolt.png")

app_title = "Shitty TFT Copy Pasta \"Tool\""

mod_copy_pasta_replacement = {
    "life": "Life",
    "defense": "Def / Defense / Defence",
    "attack": "Attack / Atk",
    "caster": "Caster",

    "fire": "Fire",
    "cold": "Cold",
    "lightning": "Lightning",
    "phys": "Phys",
    "chaos": "Chaos",

    "crit": "Crit",
    "speed": "Speed",
    "influence": "Influence / Infl",
    "random": "Random (Leo Slam)",

    "kpref": "Reforge, Keep Pref / Prefix",
    "ksuff": "Reforge, Keep Suff / Suffix",
    "pref1/3": "Fracture Prefix 1/3",
    "suff1/3": "Fracture Suffix 1/3",
    "1/5": "Fracture 1/5",

    "changeres": "Change Resist",

    "red": "Non-Red to Red",
    "blue": "Non-Blue to Blue",
    "green": "Non-Green to Green",
    "white": "Non-White to White"
}

aug_method_text = "Aug / Augment : \n{}"
remove_method_text = "Rem / Remove : \n{}"
rem_add_method_text = "Rem / Remove + Add : \n{}"

price_amount_distance = 4