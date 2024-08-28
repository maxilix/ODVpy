import os
# os.chdir("../")

import cv2
import numpy as np

from minimap.regression import poly_reg, apply_poly

# IMAGE = cv2.imread("extract_borders.bmp", cv2.IMREAD_UNCHANGED)
IMAGE = cv2.imread("motif/minimap_2.bmp", cv2.IMREAD_UNCHANGED)
SUB_H = 1
SUB_W = 1
DEGREE = 2


def sub_image(y, x):
    sub = IMAGE[y:y+SUB_H, x:x+SUB_W]
    return sub


def has_black(_image):
    target_color = np.array([0, 0, 0], dtype=np.uint8)
    mask = np.all(_image == target_color, axis=-1)
    return np.any(mask)


def mean(image):
    mean_b = np.mean(image[:, :, 0])
    mean_g = np.mean(image[:, :, 1])
    mean_r = np.mean(image[:, :, 2])
    return mean_b, mean_g, mean_r


def bright_stdev(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    stdev = np.std(gray_image)
    return stdev


def generate_image(_mean, _stdev, _height=SUB_H, _width=SUB_W):
    # generate empty image
    rop = np.zeros((_height, _width, 3), dtype=np.uint8)

    mean_b, mean_g, mean_r = _mean
    # generate chanel
    b_channel = np.full((_height, _width), mean_b, dtype=np.float32)
    g_channel = np.full((_height, _width), mean_g, dtype=np.float32)
    r_channel = np.full((_height, _width), mean_r, dtype=np.float32)

    bright = np.random.normal(0, _stdev, (_height, _width))

    # clip arrays to [0, 255]
    b_channel = np.clip(b_channel+bright, 0, 255).astype(np.uint8)
    g_channel = np.clip(g_channel+bright, 0, 255).astype(np.uint8)
    r_channel = np.clip(r_channel+bright, 0, 255).astype(np.uint8)

    # combine in the result image
    rop[:, :, 0] = b_channel
    rop[:, :, 1] = g_channel
    rop[:, :, 2] = r_channel

    return rop


h, w, _ = IMAGE.shape
source = []
target = []

for y in range(h-SUB_H+1):
    # print(f"{y}")
    for x in range(w-SUB_W+1):
        # print(f"{x=}")
        if not has_black((si:=sub_image(y, x))):
            source.append([x,y])
            target.append(mean(si))

c = poly_reg(source, target, DEGREE)
source = [[i,j] for i in range(int(h/SUB_H)) for j in range(int(w/SUB_W))]
rop = apply_poly(source, c, DEGREE).astype(np.uint8)
rop = rop.reshape(int(h/SUB_H), int(w/SUB_W), 3)

cv2.imwrite(f"g2_h{SUB_H}_w{SUB_W}_d{DEGREE}.bmp", rop)

# cv2.imshow("", rop)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

