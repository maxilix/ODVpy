import hashlib
import shutil
import os

from settings import *


class InvalidHashError(BaseException):
    pass


def backup_original():
    pass


def check_installation(root_path):
    for filename in ORIGINAL_HASH:
        complete_filename = os.path.join(root_path, filename)
        if os.path.exists(complete_filename) is False:
            raise FileNotFoundError(f"Can't find {complete_filename}")
        with open(complete_filename, "rb") as f:
            if hashlib.file_digest(f, 'sha256').hexdigest() != ORIGINAL_HASH[filename]:
                raise InvalidHashError(f"Invalid hash for {complete_filename}")
    return True



