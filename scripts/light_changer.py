from odv.level import BackupedLevel
import numpy as np
from collections import defaultdict
from PIL import Image


def mean(int_list):
    s = sum(int_list)
    return int(s / len(int_list))


def color565_mean(color_list):
    r = mean([(c >> 11) for c in color_list])
    g = mean([((c >> 5) & 0x3F) for c in color_list])
    b = mean([(c & 0x1F) for c in color_list])
    return (r << 11) + (g << 5) + b


def color565_distance(c1, c2):
    dr = abs((c1 >> 11) - (c2 >> 11))
    dg = abs(((c1 >> 5) & 0x3F) - ((c2 >> 5) & 0x3F))
    db = abs((c1 & 0x1F) - (c2 & 0x1F))
    return dr + dg + db


def interpolate_nearest_neighbor(color, data):
    closest_key = min(data.keys(), key=lambda color_key: color565_distance(color, color_key))
    return data[closest_key]


def apply_transform(color):
    try:
        return transform[color]
    except KeyError:
        return interpolate_nearest_neighbor(color, transform)


def sepia(level_id: int) -> Image:
    img = Image.open(f"./extracted/level_map/{level_id:02}.bmp")
    width, height = img.size

    pixels = img.load()  # create the pixel map
    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))

            tr = min(int(0.393 * r + 0.769 * g + 0.189 * b), 255)
            tg = min(int(0.349 * r + 0.686 * g + 0.168 * b), 255)
            tb = min(int(0.272 * r + 0.534 * g + 0.131 * b), 255)

            pixels[px, py] = (tr, tg, tb)

    img.show()


transform = defaultdict(list)
# Sanchez fortress
# ref_level = (10, 14)  # day to night
# ref_level = (14, 10)  # night to day

# Socorro
# ref_level = (15, 16)  # day to night
# ref_level = (16, 15)  # night to day

# Grants
ref_level = (18, 21)  # day to sunset
# ref_level = (21, 18)  # sunset to day

level_to_apply = 18

print("Reading")
l1 = BackupedLevel(ref_level[0])
data_1 = l1.dvm.data
l2 = BackupedLevel(ref_level[1])
data_2 = l2.dvm.data
for k, v in zip(data_1, data_2):
    transform[k].append(v)

print("Synthetizing")
transform = {k: color565_mean(v) for k, v in transform.items()}

print("Applying")
l3 = BackupedLevel(level_to_apply)
data_3 = l3.dvm.data
modify_data_3 = [apply_transform(c) for c in data_3]

print("Saving")
l3.dvm.data = modify_data_3
l3.dvm.extract_to_bmp(f"./extracted/custom_maps/{level_to_apply:02}.bmp")

print("Done")
