import hashlib
import os
import random


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


def temp_file_name(prefix=".", suffix=".temp", alphabet="0123456789abcdef", length=8):
    temp_filename = ""
    while os.path.exists(temp_filename):
        temp_filename = prefix + "".join([random.choice(alphabet) for _ in range(length)]) + suffix
    # temp_file = open(temp_filename, "w")
    # temp_file.close()
    return temp_filename


def print_original_hash_dict(installation_path):
    filenames = list_files(installation_path,
                           filename_filter=lambda filename: extension(filename) in ["scb", "dvd", "dvm"])
    print("ORIGINAL_HASH = {", end="")
    for filename in filenames:
        f = filename.replace(installation_path, "")[1:]
        f = f.replace("/", "{os.sep}")
        with open(filename, 'rb') as file:
            h = hashlib.file_digest(file, 'sha256').hexdigest()
        print(f"\n    f\"{f}\":\n        \"{h}\",", end="")
    print("\b}")
