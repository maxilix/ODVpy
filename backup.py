# import hashlib
# import shutil
# import os
#
# from odv.level import Level
# from settings import *
# from config import CONFIG
#
# def check_installation(root_path):
#     # if root_path is None:
#     #     root_path = CONFIG.installation_path
#     for filename in ORIGINAL_HASH:
#         complete_filename = os.path.join(root_path, filename)
#         if os.path.exists(complete_filename) is False:
#             raise FileNotFoundError(f"Can't find {complete_filename}")
#         with open(complete_filename, "rb") as f:
#             if hashlib.file_digest(f, 'sha256').hexdigest() != ORIGINAL_HASH[filename]:
#                 raise InvalidHashError(f"Invalid hash for {complete_filename}")
#     return True
#
#
# def copy(source, destination):
#     # source_filename = os.path.join(CONFIG.installation_path, filename)
#     # destination_filename = os.path.join("backup", filename)
#     os.makedirs(os.path.dirname(destination), exist_ok=True)
#     shutil.copy2(source, destination)
#
#
# def check_original_level(source, index):
#     # level = OriginalLevel(index)
#     v = filter(lambda x: f"{index:02}" in x, ORIGINAL_HASH.keys())
#     complete_filename = os.path.join(source, level.abs_name)
#     if source == CONFIG.installation_path
#         pass
#     pass
#
#
# def backup_original_level(index):
#     check_original_level(CONFIG.installation_path, index)
#     source = os.path.join(CONFIG.installation_path)
#     copy(CONFIG.installation_path, os.path.join(CONFIG.installation_path, level.abs_name))
#
#
# def restore_original_level(index):
#     pass
#
#
# def insert_level(level):
#     pass
#
#
# def insert_mission(root_path, level:Level):
#     filename_we = os.path.join(root_path, level.abs_name)
#
#
#
#
#
# def backup_all_level():
#     # check_all_level in installation
#     # copy_all_level
#     pass
#
# def restore():
#     # check the level in backup
#     # copy
#     pass
#
# def insert_level():
#     pass