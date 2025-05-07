from common import *
from odv.odv_object import OdvObject
from ..parser.dvm_parser import DvmParser

from odv.section import Section



class Bgnd(Section, OdvObject):
	_section_name = "BGND"
	_section_version = 4

	def _load(self, substream: ReadStream, * , abs_filename) -> None:
		size = substream.read(UShort)
		self.dvm_filename = substream.read(String, size)
		_dvm_filename = os.path.join(os.path.dirname(abs_filename), self.dvm_filename.lower() + ".dvm")
		dvm_stream = ReadStream.from_file(_dvm_filename)
		self.map_image = dvm_stream.read(Image)
		self.minimap_image = substream.read(Image)

	def _save(self, substream: WriteStream) -> None:
		substream.write(UShort(len(self.dvm_filename)))
		substream.write(String(self.dvm_filename))
		substream.write(self.minimap_image)






