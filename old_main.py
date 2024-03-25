#!/usr/bin/enc python3

import logging

from PIL import Image

from PyQt6.QtCore import Qt, QSize, QPoint, QLineF, QRectF, QPointF
from PyQt6.QtGui import QImage, QPixmap, QPolygonF
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QLabel, QGraphicsPixmapItem, QGraphicsLineItem
from PyQt6.QtGui import QPen, QBrush, QColor

import bz2

from settings import LEVEL, LOG_FILENAME
from debug import *

from common import *
from dvd import DvdParser
from dvm import DvmParser

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

a = Coordinate(600, 350)
b = Coordinate(1050, 1250)
ab = Segment(a, b)


def show_segments(i, j):
    dvm.level_map.unbuild()
    for s in dvd.move.layer_list[i].sublayer_list[j].segment_list:
        dvm.level_map.draw_segment(s)
    dvm.level_map.show()


def show_allowed_area(i, j):
    dvm.level_map.unbuild()
    area = dvd.move.layer_list[i].sublayer_list[j].allowed_area
    dvm.level_map.draw_area(area)
    for a in dvd.move.layer_list[i].sublayer_list[j].objectA_list_list[0]:
        dvm.level_map.draw_cross(a.coor)
    dvm.level_map.show()


def show_disallowed_area(i, j, k):
    dvm.level_map.unbuild()
    area = dvd.move.layer_list[i].sublayer_list[j].disallowed_area_list[k]
    dvm.level_map.draw_area(area)
    for a in dvd.move.layer_list[i].sublayer_list[j].objectA_list_list[k+1]:
        dvm.level_map.draw_cross(a.coor)
        for b_index in a.objectB_index_list:
            b = dvd.move.objectB_list[b_index]
            s = Segment(dvd.move.get_ObjectA(b.indexes_1).coor, dvd.move.get_ObjectA(b.indexes_2).coor)
            dvm.level_map.draw_segment(s)
    dvm.level_map.show()


def show_movable_mask(i):
    size = dvm.size
    dvd.move.layer_list[i].build(*size)
    dvd.move.layer_list[i].movable_mask.bmp.show()


def show_movable_mask_on_map(i):
    dvm.level_map.unbuild()

    size = dvm.size
    dvd.move.layer_list[i].build(*size)
    mask = dvd.move.layer_list[i].movable_mask.bmp.convert("L")
    dvm.level_map.build()
    level_bmp = dvm.level_map.bmp

    true_color = "#ff00002f"
    false_color = "#00000000"
    level_bmp = level_bmp.convert("RGBA")
    red = Image.new("RGBA", size, true_color)
    t = Image.new("RGBA", size, false_color)
    t.paste(red, mask=mask)
    level_bmp.paste(t, (0, 0), t)

    level_bmp.show()
    #level_bmp.save(f"./extracted/level_movable_mask/{level.index:02}_{i:02}.bmp")


match 2:
    case 0:
        level_index = int(sys.argv[1])
        level = LEVEL[level_index]
        dvm = DvmParser(level.dvm)
        dvd = DvdParser(level.dvd)
        #dvd.mask.p_build()

    case 1:
        for level in LEVEL:
            print(f"L{level.index:02} ",end="")
            dvm = DvmParser(level.dvm)
            dvd = DvdParser(level.dvd)
            print()

    case 2:
        app = QApplication(sys.argv)

        level_index = int(sys.argv[1])
        level = LEVEL[level_index]
        dvm = DvmParser(level.dvm)
        data = bz2.decompress(dvm.level_map._data)

        img = QImage(data, dvm.level_map.width, dvm.level_map.height, QImage.Format.Format_RGB16)
        w = QLabel()
        w.setPixmap(QPixmap.fromImage(img))
        w.show()
        app.exec()

    case "save":
        for level in LEVEL:
            dvm = DvmParser(level.dvm)
            dvd = DvdParser(level.dvd)
            for i in range(len(dvd.move.layer_list)):
                save_movable_mask_on_map(i)


# print(f"L{level.index:02} nb layer0.sub0.dis={len(dvd.move.layer_list[0].sublayer_list[0].disallowed_area_list)}")

# dr_seg(0,0)


# for i, gl in enumerate(dvd.move.grid_layer_list):
#	for j, ml in enumerate(gl.move_layer_list):
#		dvm.level_map.reset_bmp()
#		dvm.level_map.draw_area(ml.area)
#		dvm.level_map.show()#ave(f"./temp/gl{i}_ml{j}.bmp")
