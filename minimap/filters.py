import cv2
import numpy as np

NEW_H = 684
NEW_W = 456


img = cv2.imread('motif/minimap_3.png')



def luminance_noise(_image, scale=30):
    # Convert the image from BGR to Lab
    image_lab = cv2.cvtColor(_image, cv2.COLOR_BGR2Lab)

    # Extract L, a, and b channels
    L = image_lab[:, :, 0].astype(float)
    a = image_lab[:, :, 1].astype(float)
    b = image_lab[:, :, 2].astype(float)

    # Apply noise on L
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


def frame(_image, offset=4, bf=3.90, gf=5.60, rf=1.85):
    h, w, _ = _image.shape
    # b = _image[:, :, 0].astype(float)/4.
    # g = _image[:, :, 1].astype(float)/5.
    # r = _image[:, :, 2].astype(float)/2.


    for i in range(offset, h-offset):  # y
        _image[i, offset] = _image[i, offset] / [bf, gf, rf]
        _image[i, w-offset-1] = _image[i, w-offset-1] / [bf, gf, rf]
    for j in range(offset+1, w-offset-1):  # y
        _image[offset, j] = _image[offset, j] / [bf, gf, rf]
        _image[h-offset-1, j] = _image[h-offset-1, j] / [bf, gf, rf]
    return _image

def add_corner(_image):
    corner = cv2.imread(('sprites/corner.png'), cv2.IMREAD_UNCHANGED)  # Lire avec canal alpha si présent

    return copy_image(_image, corner, 0, 0)



def copy_image(_image1, _image2, i, j):
    src_height, src_width = _image2.shape[:2]

    if i + src_height <= _image1.shape[0] and j + src_width <= _image1.shape[1]:
        if _image2.shape[2] == 4:  # with alpha
            src_rgb = _image2[:, :, :3]
            alpha = _image2[:, :, 3] / 255.0

            # get region of interest (as pointer)
            roi = _image1[i:i + src_height, j:j + src_width]

            for c in range(3):  # for each channel (RGB)
                roi[:, :, c] = alpha * src_rgb[:, :, c] + (1 - alpha) * roi[:, :, c]
        else:  # without alpha
            _image1[i:i + src_height, j:j + src_width] = _image2

        return _image1
    else:
        raise Exception("The copied image is outside the source image")




img = luminance_noise(img)
c = max(NEW_H, NEW_W)
img = cv2.resize(img, (c, c), interpolation=cv2.INTER_CUBIC)
img = img[:NEW_H, :NEW_W]  # crop
img = mean_curvature_blur(img)
img = luminance_noise(img, scale=5)
img = frame(img)
img = add_corner(img)

cv2.imshow('', img)
cv2.waitKey(0)
cv2.destroyAllWindows()