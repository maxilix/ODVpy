import math

import cv2
import numpy as np


def luminance_noise(_image, scale=30):
    # Convert the image from BGR to Lab
    image_lab = cv2.cvtColor(_image, cv2.COLOR_BGR2Lab)

    # Extract L, a, and b channels
    L = image_lab[:, :, 0].astype(float)
    a = image_lab[:, :, 1].astype(float)
    b = image_lab[:, :, 2].astype(float)

    # Apply noise on L
    np.random.seed(42)
    L = np.clip(L+np.random.normal(scale=scale, size=L.shape), 0, 255)

    # Rebuild Lab image
    rop = np.zeros(_image.shape, dtype=np.uint8)
    rop[:, :, 0] = L
    rop[:, :, 1] = a
    rop[:, :, 2] = b

    return cv2.cvtColor(rop, cv2.COLOR_Lab2BGR)


def mean_curvature_blur(_image, sigma=0.8, alpha=0.2):
    """
    Apply Mean Curvature Blur filter to the image using OpenCV.

    Parameters:
        _image (numpy.ndarray): Input image (grayscale or color).
        sigma (float): Standard deviation for Gaussian smoothing.
        alpha (float): Weighting factor for the curvature term.
    Returns:
        numpy.ndarray: Blurred image.
    """
    img = _image.astype(np.float32)
    laplacian_image = cv2.Laplacian(img, cv2.CV_32F)

    # Update the image with the mean curvature term
    img -= alpha * laplacian_image

    # Apply Gaussian smoothing
    smoothed_image = cv2.GaussianBlur(img, (0, 0), sigmaX=sigma)

    return np.clip(smoothed_image, 0, 255).astype(np.uint8)


def add_frame(_image, offset=4, bf=3.90, gf=5.60, rf=1.85):
    rop = _image.copy()
    h, w, _ = rop.shape

    for i in range(offset, h-offset):  # y
        rop[i, offset] = rop[i, offset] / [bf, gf, rf]
        rop[i, w-offset-1] = rop[i, w-offset-1] / [bf, gf, rf]
    for j in range(offset+1, w-offset-1):  # x
        rop[offset, j] = rop[offset, j] / [bf, gf, rf]
        rop[h-offset-1, j] = rop[h-offset-1, j] / [bf, gf, rf]
    return rop


def add_corner(_image):
    corner = cv2.imread(('sprites/corner.png'), cv2.IMREAD_UNCHANGED)  # with alpha

    return copy_image(_image, corner, 0, 0)


def add_gray_map(_minimap_image, _gray_map_image, lighten=False):
    assert _minimap_image.shape[0] == _gray_map_image.shape[0] + 10
    assert _minimap_image.shape[1] == _gray_map_image.shape[1] + 10
    _gray_map_image = _gray_map_image.astype(float) / 255

    if lighten:
        def f(x):
            # return x
            # return min(-0.52*x**3 + 0.03*x**2 + 1.46*x, 1)
            return min(-0.49*x**3 - 0.24*x**2 + 1.73*x, 1)
            # return 0.1 * math.exp(-10*x) + x
        np_f = np.vectorize(f)
        _gray_map_image = np_f(_gray_map_image)

    # add gradient to the edge
    h, w = _gray_map_image.shape
    p = [3.8, 2.9, 2.2, 1.7, 1.4, 1.2, 1.1]
    for offset in range(len(p)):
        for i in range(offset, h - offset):  # y
            _gray_map_image[i, offset] = 1-(1-_gray_map_image[i, offset]) / p[offset]
            _gray_map_image[i, w - offset - 1] = 1-(1-_gray_map_image[i, w - offset - 1]) / p[offset]
        for j in range(offset + 1, w - offset - 1):  # x
            _gray_map_image[offset, j] = 1-(1-_gray_map_image[offset, j]) / p[offset]
            _gray_map_image[h - offset - 1, j] = 1-(1-_gray_map_image[h - offset - 1, j]) / p[offset]


    rop = _minimap_image.copy()
    roi = rop[5:-5, 5:-5]
    b = roi[:, :, 0].astype(float)/255
    g = roi[:, :, 1].astype(float)/255
    r = roi[:, :, 2].astype(float)/255

    G = 1.2
    roi[:, :, 0] = (b * _gray_map_image**(G*1.25)) * 255
    roi[:, :, 1] = (g * _gray_map_image**(G*0.95)) * 255
    roi[:, :, 2] = (r * _gray_map_image**(G*0.75)) * 255

    return rop


def copy_image(_image1, _image2, i, j):
    rop = _image1.copy()
    src_height, src_width = _image2.shape[:2]

    if i + src_height <= rop.shape[0] and j + src_width <= rop.shape[1]:
        if _image2.shape[2] == 4:  # with alpha
            src_rgb = _image2[:, :, :3]
            alpha = _image2[:, :, 3] / 255.0

            # get region of interest (as pointer)
            roi = rop[i:i + src_height, j:j + src_width]

            for c in range(3):  # for each channel (RGB)
                roi[:, :, c] = alpha * src_rgb[:, :, c] + (1 - alpha) * roi[:, :, c]
        else:  # without alpha
            rop[i:i + src_height, j:j + src_width] = _image2

        return rop
    else:
        raise Exception("The copied image is outside the source image")


def sharpen(_image, r1_f, r2_f):

    sharpen_kernel = np.array([[ 0, 0, 0, 0, 0],
                               [ 0, 0, 0, 0, 0],
                               [ 0, 0, 1, 0, 0],
                               [ 0, 0, 0, 0, 0],
                               [ 0, 0, 0, 0, 0]]).astype(np.float64) + \
                     np.array([[ 0, 0, 0, 0, 0],
                               [ 0, 0,-1, 0, 0],
                               [ 0,-1, 4,-1, 0],
                               [ 0, 0,-1, 0, 0],
                               [ 0, 0, 0, 0, 0]]).astype(np.float64) * r1_f + \
                     np.array([[ 0, 0,-1, 0, 0],
                               [ 0,-1, 0,-1, 0],
                               [-1, 0, 8, 0,-1],
                               [ 0,-1, 0,-1, 0],
                               [ 0, 0,-1, 0, 0]]).astype(np.float64) * r2_f


    _image_hsv = cv2.cvtColor(_image, cv2.COLOR_BGR2HSV)
    v = _image_hsv[:, :, 2]
    sharp_v = cv2.filter2D(v, -1, sharpen_kernel)
    _image_hsv[:, :, 2] = sharp_v
    return cv2.cvtColor(_image_hsv, cv2.COLOR_HSV2BGR)



def gray(_image):
    def f(x):
        return math.sin(math.pi * x / 2)
    np_f = np.vectorize(f)

    # move to [-1 ; 1]
    _gray = cv2.cvtColor(_image, cv2.COLOR_BGR2HLS)[:, :, 1].astype(np.float64)/128. - 1
    print(np.mean(_gray.reshape(-1)))
    _gray = np_f(_gray)
    print(np.mean(_gray.reshape(-1)))



    return (_gray+1)*128




level_id = [15,21,9]
stack = []

# print(f"Level {level_id:02}", end="")
for i in level_id:
    map = cv2.imread(f"../extracted/maps/{i:02}.bmp")
    f = 300/max(map.shape[0], map.shape[1])
    map = cv2.resize(map, (int(map.shape[1]*f), int(map.shape[0]*f)), interpolation=cv2.INTER_AREA)
    map = gray(map)


    stack.append(map)

rop = np.vstack(stack)



#
# map15 = cv2.imread(f"../extracted/maps/15.bmp")
# map21 = cv2.imread(f"../extracted/maps/21.bmp")
# map09 = cv2.imread(f"../extracted/maps/09.bmp")
# map = cv2.imread(f"./3_maps.png")



# minimap_max_side_length = 310
# map_max_side_length = max(map.shape[0], map.shape[1])
# f = (minimap_max_side_length-10)/map_max_side_length
# resized_map = cv2.resize(map, (int(map.shape[1]*f), int(map.shape[0]*f)), interpolation=cv2.INTER_AREA)
# resized_map = sharpen(resized_map, 0.2, 0.1)
# V = cv2.cvtColor(map, cv2.COLOR_BGR2HSV)[:, :, 2]
# L = cv2.cvtColor(map, cv2.COLOR_BGR2HLS)[:, :, 1]


# h, w = resized_gray_map.shape
# h += 10
# w += 10
#
# minimap = cv2.imread("sprites/gradient.png")
# minimap = luminance_noise(minimap)
# c = max(h, w)
# minimap = cv2.resize(minimap, (c, c), interpolation=cv2.INTER_CUBIC)
# minimap = minimap[:h, :w]  # crop
# minimap = mean_curvature_blur(minimap)
# minimap = luminance_noise(minimap, scale=5)
# minimap = add_frame(minimap)
# minimap = add_gray_map(minimap, resized_gray_map, lighten=False)
# minimap = add_corner(minimap)


# minimap = cv2.cvtColor(minimap, cv2.COLOR_BGR2BGR565)
# print(minimap.shape)
# print(minimap.tobytes()[:2].hex())


cv2.imwrite(f"stack.png", rop)
# cv2.imwrite(f"L.png", L)
# cv2.imwrite(f"rebuilt/{level_id:02}.bmp", minimap)
# print(" - Done")

# cv2.imwrite(f"test.png", minimap)
