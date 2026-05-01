import os
import random
import re
import shutil
from pathlib import Path


def auto_id(key):
    auto_id.id[key] = auto_id.id.get(key, -1) + 1
    return auto_id.id[key]
auto_id.id = dict()


def extension(filename):
    try:
        return filename.rsplit(".", 1)[1].lower()
    except IndexError:
        return None



def remove_extension(filename):
    if (ext := extension(filename)) is not None:
        return filename.replace(f".{ext}", "")
    else:
        return filename



def temp_filename(prefix=".", suffix=".temp", alphabet="0123456789abcdef", length=8):
    rop = ""
    while os.path.exists(rop):
        rop = prefix + "".join([random.choice(alphabet) for _ in range(length)]) + suffix
    # temp_file = open(temp_filename, "w")
    # temp_file.close()
    return rop



def copy(source:Path, destination:Path):
    if source != destination:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def original_filename(index: int, root: Path) -> Path:
    assert 0 <= index <= 25
    filename = root
    if index == 0:
        filename = filename / "demo"
    filename /= "data"
    filename /= "levels"
    filename /= f"level_{index:02}"
    return filename


def guess_level_index(filename: Path|str) -> int:
    try:
        m = re.findall(r"_(\d\d)", str(filename))
        return int(m[-1])
    except IndexError:
        # print("[Level] Level index cannot be found")
        return -1
