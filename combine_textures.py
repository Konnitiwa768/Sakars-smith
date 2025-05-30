import os
from PIL import Image

parts_dir = "parts"
output_dir = "Resourcepack/textures/item"
os.makedirs(output_dir, exist_ok=True)

sticks = [f for f in os.listdir(parts_dir) if f.endswith("stick.png")]
fronts = [f for f in os.listdir(parts_dir) if f.endswith("pickaxe.png") or f.endswith("sword.png")]

for stick in sticks:
    stick_img = Image.open(os.path.join(parts_dir, stick)).convert("RGBA")
    for front in fronts:
        front_img = Image.open(os.path.join(parts_dir, front)).convert("RGBA")
        if front_img.size != stick_img.size:
            front_img = front_img.resize(stick_img.size)
        combined = Image.alpha_composite(stick_img, front_img)
        out_name = f"{os.path.splitext(front)[0]}_{os.path.splitext(stick)[0]}.png"
        combined.save(os.path.join(output_dir, out_name))
