import os

os.chdir("../")

import cv2

# map_size_x = []
# map_size_y = []
# minimap_size_x = []
# minimap_size_y = []
#
# for level_index in range(26):
#     print(f"\nLevel {level_index}")
#     level = BackupedLevel(level_index)
#     map_size_x.append(level.dvm.level_map.width)
#     map_size_y.append(level.dvm.level_map.height)
#     minimap_size_x.append(level.dvd.bgnd.minimap.width())
#     minimap_size_y.append(level.dvd.bgnd.minimap.height())

map_size_x =     [2560, 2112, 1600, 1920, 2560, 1280, 2368, 2112, 2240, 1600, 1600, 1280, 2240, 2368, 1600, 2240, 2240, 1600, 2560, 1280, 1280, 2560, 2432, 2432, 2944, 1024]
map_size_y =     [1600, 1088, 2368,  896, 1408,  768, 1920, 1088, 1600, 1472, 2240, 2368, 1728, 1728, 1408, 1600, 1600, 1024, 1728, 2240,  768, 1728, 1792, 1856, 1664,  960]
minimap_size_x = [ 300,  300,  207,  300,  300,  300,  300,  300,  300,  300,  218,  167,  300,  300,  300,  300,  300,  300,  300,  176,  300,  300,  300,  300,  300,  150]
minimap_size_y = [ 192,  159,  300,  145,  170,  184,  245,  159,  218,  278,  300,  300,  234,  223,  265,  217,  218,  197,  207,  300,  184,  207,  226,  231,  175,  142]


def print_reduction_factor():
    for i in range(25):
        factor = max(map_size_x[i], map_size_y[i])/290
        print(f"Level_{i:02}  f={round(factor,3)}")
        print(f"  x: {round(map_size_x[i]/factor) + 10} == {minimap_size_x[i]}")
        print(f"  y: {round(map_size_y[i]/factor) + 10} == {minimap_size_y[i]}")

    i = 25
    factor = max(map_size_x[i], map_size_y[i])/140
    print(f"Level_{i:02}  f={round(factor,3)}")
    print(f"  x: {round(map_size_x[i]/factor) + 10} == {minimap_size_x[i]}")
    print(f"  y: {round(map_size_y[i]/factor) + 10} == {minimap_size_y[i]}")


def load_images(_path, _indexes, _suffixe):
    filenames = [f"{_path}{i:02}{_suffixe}" for i in _indexes]
    images = [cv2.imread(file) for file in filenames]
    return images


path = "extracted/map_to_minimap/"
indexes = [0]

original_images = load_images(path, indexes, "map.bmp")
filtered_images = load_images(path, indexes, "minimap.bmp")