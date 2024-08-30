from PyQt6.QtGui import QImage

from common import *


def image_to_qimage(image: Image):
    h = image.height
    w = image.width
    return QImage(image.rgba().data, w, h, 4*w, QImage.Format.Format_RGBA8888)