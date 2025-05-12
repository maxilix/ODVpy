from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QColor

from common import *

def same_type(l):
    return l==[] or all([type(l[0] == type(e) for e in l)])

def checkstate_from_list(l):
    if all(l):
        return Qt.CheckState.Checked
    elif any(l):
        return Qt.CheckState.PartiallyChecked
    else:
        return Qt.CheckState.Unchecked

def bounding_rect_of(graphic_list):
    rect = graphic_list[0].boundingRect()
    for g in graphic_list[1:]:
        rect = rect.united(g.boundingRect())
    return rect

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


