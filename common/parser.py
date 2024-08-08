import hashlib
import io
import os

from .rw_stream import ReadStream
from .utils import extension


extension_list = ["dvf", "dvm", "dvd"]


class Parser(object):

	ext = None   # must be defined by inheriting objects
	modified = False

	def __init__(self, filename):
		assert extension(filename) == self.ext
		# if os.sep in filename:
		# 	temp_name = filename.rsplit(os.sep, 1)[1][:-4]
		# else:
		# 	temp_name = filename[:-4]
		self.filename = filename  # temp_name.replace(" ", "_")
		self.stream = ReadStream.from_file(self.filename)
		# log.info(f"Parse {filename}")

	def __repr__(self):
		return f"<Parser {self.ext} : {self.filename}>"

	def hash(self):
		# data = io.FileIO(self.stream.get_value())
		with open(self.filename, "rb") as f:
			rop = hashlib.file_digest(f, 'sha256').hexdigest().lower()
		return rop

	def save_to_file(self, filename):
		pass
