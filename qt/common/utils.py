from PyQt6.QtGui import QImage, QColor

from common import *


def image_to_qimage(image: Image):
    h = image.height
    w = image.width
    return QImage(image.rgba().data, w, h, 4*w, QImage.Format.Format_RGBA8888)

def maskimage_to_qimage(maskimage: MaskImage, true_color=(0,0,0)):
    if isinstance(true_color, QColor):
        true_color = true_color.rgb()
    h = maskimage.height
    w = maskimage.width
    return QImage(maskimage.rgba(true_color).data, w, h, 4*w, QImage.Format.Format_RGBA8888)


