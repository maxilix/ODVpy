from config import Config
from old_code.old_dvf import DvfParser

Config.load()


# level = Level("./dev/empty_level/empty_level_02")
# level = Level("../Missions/03_Red_River/level_03")
# level = Level("../Missions/00_All_Character/level_00")
# level = InstalledLevel(2)
# level = BackupedLevel(4)




dvf = DvfParser("./scripts/accessories.dvf")
for s in dvf.sprites[350:360]:
    s.build()
    s.bmp.show()
