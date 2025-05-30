import os
import json

# アイテムの基礎データ
ITEM_STATS = {
    "wooden_pickaxe":    {"durability": 59,   "damage": 2, "efficiency": 2,  "mining_speed": 2},
    "stone_pickaxe":     {"durability": 131,  "damage": 3, "efficiency": 4,  "mining_speed": 4},
    "iron_pickaxe":      {"durability": 250,  "damage": 4, "efficiency": 6,  "mining_speed": 6},
    "golden_pickaxe":    {"durability": 32,   "damage": 2, "efficiency": 12, "mining_speed": 12},
    "karmesine_pickaxe":     {"durability": 1244,  "damage": 7, "efficiency": 6,  "mining_speed": 7},
    "diamond_pickaxe":   {"durability": 1561, "damage": 5, "efficiency": 8,  "mining_speed": 8},
    "netherrite_pickaxe":{"durability": 2031, "damage": 6, "efficiency": 9,  "mining_speed": 9},
    "bone_pickaxe":      {"durability": 100,  "damage": 3, "efficiency": 3,  "mining_speed": 3},
    "wooden_sword":      {"durability": 59,   "damage": 4, "efficiency": 1,  "mining_speed": 1},
    "stone_sword":       {"durability": 131,  "damage": 5, "efficiency": 1,  "mining_speed": 1},
    "karmesin_sword":       {"durability": 1244,  "damage": 9, "efficiency": 1,  "mining_speed": 1},
    "iron_sword":        {"durability": 250,  "damage": 6, "efficiency": 1,  "mining_speed": 1},
    "golden_sword":      {"durability": 32,   "damage": 4, "efficiency": 1,  "mining_speed": 1},
    "diamond_sword":     {"durability": 1561, "damage": 7, "efficiency": 1,  "mining_speed": 1},
    "netherrite_sword":  {"durability": 2031, "damage": 8, "efficiency": 1,  "mining_speed": 1},
    "bone_sword":        {"durability": 100,  "damage": 4, "efficiency": 1,  "mining_speed": 1},
}

# stickごとの倍率テーブル
STICK_MULTIPLIERS = {
    "wooden_stick":     {"durability": 1.0, "damage": 1.0, "efficiency": 1.0},
    "stone_stick":      {"durability": 1.2, "damage": 1.1, "efficiency": 1.05},
    "iron_stick":       {"durability": 1.5, "damage": 1.2, "efficiency": 1.15},
    "golden_stick":     {"durability": 0.8, "damage": 1.5, "efficiency": 1.3},
    "diamond_stick":    {"durability": 2.0, "damage": 1.4, "efficiency": 1.4},
    "karmesin_stick":     {"durability": 0.95, "damage": 2.7, "efficiency": 1.9},
    "netherrite_stick": {"durability": 2.5, "damage": 2.0, "efficiency": 2.0},
    "bone_stick":       {"durability": 1.3, "damage": 1.2, "efficiency": 1.1},
    # 必要に応じて追加
}

parts_dir = "parts"
json_out_dir = "behavior_pack/items"
os.makedirs(json_out_dir, exist_ok=True)

sticks = [f for f in os.listdir(parts_dir) if f.endswith("stick.png")]
fronts = [f for f in os.listdir(parts_dir) if f.endswith("pickaxe.png") or f.endswith("sword.png")]

for stick in sticks:
    stick_base = os.path.splitext(stick)[0]
    multiplier = STICK_MULTIPLIERS.get(stick_base, {"durability": 1.0, "damage": 1.0, "efficiency": 1.0})

    for front in fronts:
        front_base = os.path.splitext(front)[0]
        item_key = front_base
        stats = ITEM_STATS.get(item_key, {"durability": 100, "damage": 3, "efficiency": 1, "mining_speed": 1})

        # 各能力値に倍率を適用
        stats2 = dict(stats)
        stats2["durability"] = int(stats["durability"] * multiplier["durability"])
        stats2["damage"] = int(stats["damage"] * multiplier["damage"])
        stats2["efficiency"] = float(stats["efficiency"] * multiplier["efficiency"])

        identifier = f"{front_base}_{stick_base}".lower()
        icon_name = identifier  # テクスチャ画像名に合わせる場合

        item_json = {
            "format_version": "1.20.0",
            "minecraft:item": {
                "description": {
                    "identifier": f"custom:{identifier}",
                    "category": "Tools"
                },
                "components": {
                    "minecraft:icon": f"textures/item/{icon_name}",
                    "minecraft:mining_speed": stats2["mining_speed"],
                    "minecraft:durability": stats2["durability"],
                    "minecraft:damage": stats2["damage"],
                    "minecraft:efficiency": stats2["efficiency"]
                }
            }
        }
        json_path = os.path.join(json_out_dir, f"{identifier}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(item_json, f, indent=2, ensure_ascii=False)
