from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QImage, QColor

from odv.common import *

def same_type(l):
    return l==[] or all([type(l[0] == type(e) for e in l)])

def checkstate_from_list(l):
    if all(l):
        return Qt.CheckState.Checked
    elif any(l):
        return Qt.CheckState.PartiallyChecked
    else:
        return Qt.CheckState.Unchecked

def bounding_rect_of(graphic_list) -> QRectF:
    rect = graphic_list[0].sceneBoundingRect()
    for g in graphic_list[1:]:
        rect = rect.united(g.sceneBoundingRect())
    return rect

def image_to_qimage(image: Image):
    h = image.height
    w = image.width
    return QImage(image.rgba().data, w, h, 4 * w, QImage.Format.Format_RGBA8888)

def mask_image_to_qimage(mask_image: MaskImage, true_color=(0, 0, 0)):
    if isinstance(true_color, QColor):
        true_color = true_color.rgb()
    h = mask_image.height
    w = mask_image.width
    return QImage(mask_image.rgba(true_color).data, w, h, 4 * w, QImage.Format.Format_RGBA8888)


