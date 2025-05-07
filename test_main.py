from config import CONFIG
from odv.level import BackupedLevel, Level

CONFIG.load()




# level = Level("./dev/empty_level/empty_level_02")
# level = Level("../Missions/03_Red_River/level_03")
# level = Level("../Missions/00_All_Character/level_00")
# level = InstalledLevel(2)
level = BackupedLevel(4)


bgnd = level.bgnd
exit()


for level_index in range(26):
    print(f"\nLevel {level_index}")
    level = BackupedLevel(level_index)

    # lift = level.dvd.lift
    # for lift_area in lift:
    #     if lift_area.lift_type == 0:
    #         print(f"L{level_index} i={lift_area.i}")

    # buildings = level.dvd.buil.buildings
    # for building in buildings:
    #     for door in building:
    #         if door.sector_3.global_id != 0:
    #             print(f"L{level_index}: building {building.i}, door {door.i}")

    bond = level.dvd.bond
    for bond_entry in bond:
        if isinstance(bond_entry.sight_obstacle_1, GroundSight) or isinstance(bond_entry.sight_obstacle_2, GroundSight):
            # print("Ground")
            pass
        else:
            print(f"{bond_entry.sight_obstacle_1.sector.parent.i} {bond_entry.sight_obstacle_2.sector.parent.i} - {bond_entry.layer.i}")

# level = Level("./dev/empty_level/empty_level_02")
# mask = level.dvd.mask

# bgnd.image.debug_show()
# level = BackupedLevel(10)


# jump_area = level.dvd.jump[4]
# for e in jump_area.jump_roof_balcony_list:
    # e.u1 = 100
    # e.u2 = 50
    # e.u3 = -30


# 134 130 -12
# 134 130 -2
# 133 130 -3




# exit()

# for sublayer in motion[0]:
#     for area in sublayer.obstacles:
#         level.dvm.draw(area.poly, QPen(QColor(255, 90, 40, 128)), QBrush(QColor(255, 90, 40, 32)))

# level.insert_in_game()
