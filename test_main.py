from config import CONFIG
from odv.level import Level

CONFIG.load()

"""
w[0] = obstacle avoidance distance, on foot
     = [x distance, y distance]
     
w[3] or w[4] = obstacle avoidance distance, on horseback
             = [x distance, y distance]
             
             
        human                    monkey       horse      

L00   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L01   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L02   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L03   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L04   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L05   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L06   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L07   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L08   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L09   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L10   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L11   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L12   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L13   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L14   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L15   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L16   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L17   [6.0, 3.0]  [11.0, 6.0]  [3.0, 2.0]  [19.0, 11.0]
L18   [6.0, 3.0]  [11.0, 6.0]              [19.0, 11.0]
L19   [6.0, 3.0]  [11.0, 6.0] 
L20   [6.0, 3.0]  [11.0, 6.0]  [3.0, 2.0]  [19.0, 11.0]
L21   [6.0, 3.0]  [11.0, 6.0]  [3.0, 2.0]  [19.0, 11.0]
L22   [6.0, 3.0]  [11.0, 6.0]  [3.0, 2.0]  [19.0, 11.0]
L23   [6.0, 3.0]  [11.0, 6.0]  [3.0, 2.0]  [19.0, 11.0]
L24   [6.0, 3.0]  [11.0, 6.0]  [3.0, 2.0]
L25   [6.0, 3.0]  [11.0, 6.0] 
"""


# def draw_obstacle_on_dvm(level, layer_index=0):
#     if level.dvd.move.loaded_areas is False:
#         level.dvd.move.load(only_areas=True)
#     pen = QPen(QColor(255, 0, 0, 128))
#     pen.setWidthF(0.5)
#     brush = QBrush(QColor(255, 0, 0, 32))
#     for sublayer in level.dvd.move[layer_index]:
#         for obstacle in sublayer:
#             level.dvm.draw(obstacle.QPolygonF(), pen, brush)




level = Level("./dev/empty_level/empty_level_02")
# level = Level("../Missions/03_Red_River/level_03")
# level = Level("../Missions/00_All_Character/level_00")
# level = InstalledLevel(2)
# level = BackupedLevel(2)


# for level_index in range(26):
#     print(f"Level {level_index}")

# move = level.dvd.move

# buil = level.dvd.buil
# print(len(buil.building_list), len(buil.special_door_list))
# for sd in buil.special_door_list:
#     print(sd.accesses[0].point, sd.accesses[0].area_global_id, sd.accesses[0].layer_id)
#     print(sd.accesses[1].point, sd.accesses[1].area_global_id, sd.accesses[1].layer_id)
#     print(sd.accesses[2].point, sd.accesses[2].area_global_id, sd.accesses[2].layer_id)
#     print()

# exit()
bond = level.dvd.bond
for bond_line in bond:
    bond_line.right_id, bond_line.left_id = bond_line.left_id, bond_line.right_id



# for sublayer in motion[0]:
#     for area in sublayer.obstacles:
#         level.dvm.draw(area.poly, QPen(QColor(255, 90, 40, 128)), QBrush(QColor(255, 90, 40, 32)))



level.insert_in_game()
