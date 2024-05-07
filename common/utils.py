import os
import random
import shutil


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


def copy(source, destination):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    shutil.copy2(source, destination)


# def copy_dvd(source, destination):
#     copy(f"{source}.dvd", f"{destination}.dvd")
#
#
# def copy_dvm(source, destination):
#     copy(f"{source}.dvm", f"{destination}.dvm")
#
# def copy_scb(source, destination):
#     copy(f"{source}.scb", f"{destination}.scb")
#
#
# def copy_stf(source, destination):
#     index_str = destination[-2:]
#     copy(f"{source[:-8]}{os.sep}briefing{os.sep}b00bs{index_str}",
#          f"{destination[:-8]}{os.sep}briefing{os.sep}b00bs{index_str}")