import os

from .rw_stream import ReadStream


extension_list = ["dvf", "dvm", "dvd"]


class Parser(object):

	extension = None   # must be defined by inheriting objects

	def __init__(self, filename):
		assert filename[-4:] == f".{self.extension}"
		if os.sep in filename:
			temp_name = filename.rsplit(os.sep, 1)[1][:-4]
		else:
			temp_name = filename[:-4]
		self.name = temp_name.replace(" ", "_")
		self.stream = ReadStream.from_file(filename)
		# log.info(f"Parse {filename}")

	def __repr__(self):
		return f"<Parser {self.extension} : {self.name}>"
