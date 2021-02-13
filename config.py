import os

prices_path = "prices.txt"
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

resist_transform_image_path = os.path.join("assets", "arrow_curved.png")
fire_image_path = os.path.join("assets", "diy_flame.png")
cold_image_path = os.path.join("assets", "snowflake.png")
lightning_image_path = os.path.join("assets", "lightning_bolt.png")

app_title = "Shitty TFT Copy Pasta \"Tool\""

mod_copy_pasta_replacement = {
    "life": "Life",
    "defense": "Def",
    "attack": "Attack",
    "caster": "Caster",

    "fire": "Fire",
    "cold": "Cold",
    "lightning": "Lightning",
    "phys": "Phys",
    "chaos": "Chaos",

    "crit": "Crit",
    "speed": "Speed",
    "influence": "Influence",

    "kpref": "Reforge, Keep Pref / Prefix / Prefixes",
    "ksuff": "Reforge, Keep Suff / Suffix / Suffixes",
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

price_amount_distance = 8