from config import CONFIG
from odv.level import BackupedLevel

CONFIG.load()


# level = Level("./dev/empty_level/empty_level_02")
# level = Level("../Missions/03_Red_River/level_03")
# level = Level("../Missions/00_All_Character/level_00")
# level = InstalledLevel(2)
# level = BackupedLevel(2)


"""
without shape:
level lift_area_id
L0 0
L0 1
L0 2
L0 3
L0 4
L0 5
L0 6
L0 7
L0 8
L0 9
L1 0
L1 1
L1 2
L1 3
L8 1
L10 1
L11 0
L11 1
L12 0
L12 4
L12 5
L12 6
L12 7
L12 8
L13 6
L13 7
L13 8
L13 9
L13 16
L15 0
L15 1
L15 4
L16 0
L16 2
L16 4
L16 5
L18 0
L18 1
L18 2
L18 3
L18 4
L18 5
L18 6
L18 7
L18 8
L18 9
L18 10
L18 11
L18 12
L21 0
L21 1
L21 2
L21 3
L21 4
L21 5
L21 6
L21 7
L21 8
L21 9
L21 10
L21 11
L22 0
L22 1
L22 2
L24 0
L24 1
L24 2
L24 3
L24 4
L24 5
L24 6
"""


for level_index in range(26):
    # print(f"Level {level_index}")
    level = BackupedLevel(level_index)

    lift = level.dvd.lift
    for lift_area in lift:
        if lift_area.lift_type == 0:
            print(f"L{level_index} i={lift_area.i}")

exit()


# for sublayer in motion[0]:
#     for area in sublayer.obstacles:
#         level.dvm.draw(area.poly, QPen(QColor(255, 90, 40, 128)), QBrush(QColor(255, 90, 40, 32)))


# level.insert_in_game()
