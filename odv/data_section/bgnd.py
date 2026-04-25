import re

from odv.common import *
from config import Config
from odv.odv_object import OdvObject
from odv.section import Section



def find_dvm_file(dvm_filename: str) -> str:
	m = re.findall(r"(\d\d)", dvm_filename)
	index = int(m[-1])
	return original_name(index, root=Config.backup_path) + ".dvm"



class Bgnd(Section, OdvObject):
	_section_id = 1
	_section_version = 4

	def _load(self, substream: ReadStream, level) -> None:
		size = substream.read(UShort)
		self.dvm_filename = substream.read(String, size)
		# _dvm_filename = os.path.join(Config.backup_path, self.dvm_filename.lower() + ".dvm")
		dvm_stream = ReadStream.from_file(find_dvm_file(self.dvm_filename))
		self.map_image = dvm_stream.read(Image)
		self.minimap_image = substream.read(Image)

	def _save(self, substream: WriteStream) -> None:
		substream.write(UShort(len(self.dvm_filename)))
		substream.write(String(self.dvm_filename))
		substream.write(self.minimap_image)






