import os
import json

def get_ingot(front_base):
    if front_base.startswith("diamond"):
        return "diamond"
    elif front_base.startswith("karmesine"):
        return "karmesine_ingot"
    else:
        return front_base.replace("_pickaxe", "_ingot").replace("_sword", "_ingot").replace("_rapier", "_ingot")

def get_ingot_prefix(ingot):
    if ingot == "karmesine_ingot":
        return "custom:"
    elif ingot == "diamond":
        return ""
    else:
        return "minecraft:"

parts_dir = "parts"
json_out_dir = "behavior_pack/recipes"
os.makedirs(json_out_dir, exist_ok=True)

fronts = [f for f in os.listdir(parts_dir) if f.endswith("pickaxe.png") or f.endswith("sword.png") or f.endswith("rapier.png")]

for front in fronts:
    front_base = os.path.splitext(front)[0]
    identifier = f"{front_base}".lower()

    ingot = get_ingot(front_base)
    ingot_prefix = get_ingot_prefix(ingot)

    if "pickaxe" in front_base:
        pattern = [
            "III",
            " I ",
            " I "
        ]
        key = {
            "I": {"item": f"{ingot_prefix}{ingot}"},
        }
    elif "sword" in front_base:
        pattern = [
            " I ",
            " I ",
            " I "
        ]
        key = {
            "I": {"item": f"{ingot_prefix}{ingot}"},
        }
    elif "rapier" in front_base:
        # レイピア独自のレシピ例（要調整）
        pattern = [
            "  I",
            " I ",
            "I  "
        ]
        key = {
            "I": {"item": f"{ingot_prefix}{ingot}"},
        }
    else:
        continue

    recipe_json = {
        "format_version": "1.20.0",
        "minecraft:recipe_shaped": {
            "description": {
                "identifier": f"custom:{identifier}"
            },
            "tags": ["crafting_table"],
            "pattern": pattern,
            "key": key,
            "result": {
                "item": f"custom:{identifier}",
                "count": 1
            }
        }
    }

    json_path = os.path.join(json_out_dir, f"{identifier}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(recipe_json, f, indent=2, ensure_ascii=False)
