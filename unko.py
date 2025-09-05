import os
import json

# 出力先
json_dir = "behavior_pack/items"
output_file = "Resourcepack/textures/item_texture.json"

# アイテム JSON をまとめる
textures = {}
if os.path.exists(json_dir):
    for fname in os.listdir(json_dir):
        if fname.endswith(".json"):
            fpath = os.path.join(json_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                identifier = data["minecraft:item"]["description"]["identifier"]
                icon_path = data["minecraft:item"]["components"]["minecraft:icon"]
                textures[identifier] = {"textures": icon_path}

item_texture_json = {
    "resource_pack_name": "unkoooooooo",
    "texture_name": "atlas.items",
    "texture_data": textures
}

# ディレクトリ作成
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# 保存
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(item_texture_json, f, indent=2, ensure_ascii=False)

print(f"Generated {output_file} with {len(textures)} items.")
