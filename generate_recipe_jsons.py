import os
import json

# スティック名からインゴット名への変換（例: "iron_stick" → "iron_ingot"）
def stick_to_ingot(stick_name):
    if stick_name.endswith("_stick"):
        return stick_name.replace("_stick", "_ingot")
    return stick_name

parts_dir = "parts"
json_out_dir = "behavior_pack/recipes"
os.makedirs(json_out_dir, exist_ok=True)

sticks = [f for f in os.listdir(parts_dir) if f.endswith("stick.png")]
fronts = [f for f in os.listdir(parts_dir) if f.endswith("pickaxe.png") or f.endswith("sword.png")]

for stick in sticks:
    stick_base = os.path.splitext(stick)[0]
    ingot = stick_to_ingot(stick_base)

    for front in fronts:
        front_base = os.path.splitext(front)[0]
        identifier = f"{front_base}_{stick_base}".lower()

        # レシピタイプ判定（例: ピッケル、ソード）
        if "pickaxe" in front_base:
            # ピッケルのレシピ
            pattern = [
                "III",
                " S ",
                " S "
            ]
            key = {
                "I": {"item": f"custom:{front_base.replace('_pickaxe', '_ingot')}"},
                "S": {"item": f"custom:{ingot}"}
            }
        elif "sword" in front_base:
            # ソードのレシピ
            pattern = [
                " I ",
                " I ",
                " S "
            ]
            key = {
                "I": {"item": f"custom:{front_base.replace('_sword', '_ingot')}"},
                "S": {"item": f"custom:{ingot}"}
            }
        else:
            continue  # 対象外

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
