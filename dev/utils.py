import hashlib
import os
import random

from common import extension
from odv.level import original_name


def list_files(path, recursive=True, *, filename_filter=lambda filename: True):
    rop = []
    try:
        filenames = os.listdir(path)
    except PermissionError:
        print(f"{path} : PermissionError")
        return []

    for filename in sorted(filenames):
        absolute_filename = os.path.join(path, filename)
        if os.path.isdir(absolute_filename) and recursive:
            rop += list_files(absolute_filename, filename_filter=filename_filter)
        else:
            if filename_filter(absolute_filename):
                rop.append(absolute_filename)

    return rop


def print_original_hash_dict(installation_path):
    filenames = list_files(installation_path,
                           filename_filter=lambda fn: extension(fn) in ["scb", "dvd", "dvm"])
    print("ORIGINAL_HASH = {", end="")
    for filename in filenames:
        f = filename.replace(installation_path, "")[1:]
        f = f.replace("/", "{os.sep}")
        with open(filename, 'rb') as file:
            h = hashlib.file_digest(file, 'sha256').hexdigest()
        print(f"\n    f\"{f}\":\n        \"{h}\",", end="")
    print("\b}")


def print_original_hash_dict_2(installation_path):
    # filenames = list_files(installation_path,
    #                        filename_filter=lambda fn: extension(fn) in ["scb", "dvd", "dvm"])
    print("ORIGINAL_LEVEL_HASH = [")
    for i in range(26):
        print("\t(", end="")
        for ext in ['dvd', 'dvm', 'scb']:  #, 'stf']:
            filename = installation_path + original_name(i) + "." + ext
            with open(filename, 'rb') as file:
                h = hashlib.file_digest(file, 'sha256').hexdigest().lower()
                print(f"\"{h}\",\n\t ", end="")
        filename = installation_path + original_name(i)[:-8] + f"/briefing/d00bs{i:02}"
        with open(filename, 'rb') as file:
            h = hashlib.file_digest(file, 'sha256').hexdigest().lower()
            print(f"\"{h}\"),")
    print("]")

print_original_hash_dict_2("/home/maxe/Documents/Desperados_WDoA/Desperados Wanted Dead or Alive")
