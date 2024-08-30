import cv2
import numpy as np
from matplotlib import pyplot as plt


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


def mean_curvature_blur(_image, sigma=0.7, alpha=0.2):
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

    # update the image with the mean curvature term
    img -= alpha * laplacian_image

    # apply gaussian smoothing
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
    corner = cv2.imread("sprites/corner.png", cv2.IMREAD_UNCHANGED)  # with alpha

    return copy_image(_image, corner, 0, 0)


def add_gray_map(_minimap_image, _gray_map_image):
    assert _minimap_image.shape[0] == _gray_map_image.shape[0] + 10
    assert _minimap_image.shape[1] == _gray_map_image.shape[1] + 10
    _gray_mask = _gray_map_image.astype(float) / 255

    # add gradient to the edge
    h, w = _gray_mask.shape
    p = [3.8, 2.9, 2.2, 1.7, 1.4, 1.2, 1.1]
    for offset in range(len(p)):
        for i in range(offset, h - offset):  # y
            _gray_mask[i, offset] = 1-(1-_gray_mask[i, offset]) / p[offset]
            _gray_mask[i, w - offset - 1] = 1-(1-_gray_mask[i, w - offset - 1]) / p[offset]
        for j in range(offset + 1, w - offset - 1):  # x
            _gray_mask[offset, j] = 1-(1-_gray_mask[offset, j]) / p[offset]
            _gray_mask[h - offset - 1, j] = 1-(1-_gray_mask[h - offset - 1, j]) / p[offset]


    rop = _minimap_image.copy()
    roi = rop[5:-5, 5:-5]
    b = roi[:, :, 0].astype(float)/255
    g = roi[:, :, 1].astype(float)/255
    r = roi[:, :, 2].astype(float)/255

    G = 1.05
    roi[:, :, 0] = (b * _gray_mask**(G*1.25)) * 255
    roi[:, :, 1] = (g * _gray_mask**(G*0.95)) * 255
    roi[:, :, 2] = (r * _gray_mask**(G*0.75)) * 255

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


def gray_n(_image, fm=None):
    # _gray = cv2.cvtColor(_image, cv2.COLOR_BGR2HLS)[:, :, 1].astype(np.float64)/255.  # Luminance
    _gray = cv2.cvtColor(_image, cv2.COLOR_BGR2HSV)[:, :, 2].astype(np.float64)/255.  # Value

    if fm is None or fm == []:
        rop = _gray
        poly = lambda x: x
    else:
        n = len(fm)
        mean = np.mean(_gray.reshape(-1))

        x = np.linspace(0,1, n+2)
        y = np.concatenate(([0], (0.5 - mean)/10*np.array(fm) + x[1:-1], [1]))

        poly = np.poly1d(np.polyfit(x, y, n+1))
        rop = poly(_gray)
    return np.clip(rop * 255, 0, 255).astype(np.uint8), poly, _gray.reshape(-1)


# for i in range(25):
i = 6
map_image = cv2.imread(f"../extracted/maps/{i:02}.bmp")
minimap_max_side_length = 300
map_max_side_length = max(map_image.shape[0], map_image.shape[1])
f = (minimap_max_side_length-10)/map_max_side_length
resized_map = cv2.resize(map_image, (int(map_image.shape[1]*f), int(map_image.shape[0]*f)), interpolation=cv2.INTER_AREA)
resized_map = sharpen(resized_map, 0.2, 0.1)
resized_gray_map, poly, lum = gray_n(resized_map, fm=[1.5, 4, 5, 3])

h, w = resized_gray_map.shape
h += 10
w += 10

minimap = cv2.imread("sprites/gradient.png")
minimap = luminance_noise(minimap)
c = max(h, w)
minimap = cv2.resize(minimap, (c, c), interpolation=cv2.INTER_CUBIC)
minimap = minimap[:h, :w]  # crop
minimap = mean_curvature_blur(minimap)
minimap = luminance_noise(minimap, scale=8)
minimap = add_frame(minimap)
minimap = add_gray_map(minimap, resized_gray_map)
minimap = add_corner(minimap)

cv2.imwrite(f"rebuilt/ign_{i:02}.png", minimap)
original_minimap = cv2.imread(f"../extracted/minimaps/{i:02}.bmp")
compare = np.hstack([original_minimap[:h,:w], minimap])
cv2.imwrite(f"compare/ign_{i:02}.png", compare)

# Output graph
step = 0.01
bins = np.arange(0, 1+step, step)
hist, edges = np.histogram(lum, bins=bins)
hist = hist/max(hist)

x_plot = np.linspace(0, 1, 100)
y_plot = np.clip(poly(x_plot), 0, 1)

plt.bar(edges[:-1], hist, width=step, alpha=0.5)
plt.plot([0,1], [0,1], color="gray")
plt.plot(x_plot, y_plot, color="red")
plt.grid(True)
plt.show()