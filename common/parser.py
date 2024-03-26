
from . import ByteStream


extension_list = ["dvf", "dvm", "dvd"]


class Parser(object):

	def __init__(self, filename):
		assert filename[-4:] == f".{self.extension}"
		if "/" in filename:
			temp_name = filename.rsplit("/",1)[1][:-4]
		else:
			temp_name = filename[:-4]
		self.name = temp_name.replace(" ", "_")
		self.stream = ByteStream.from_file(filename)
		# log.info(f"Parse {filename}")

	def __repr__(self):
		return f"<Parser {self.extension} : {self.name}>"
