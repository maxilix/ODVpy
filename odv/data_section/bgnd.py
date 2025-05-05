from common import *
from odv.odv_object import OdvObject

from odv.section import Section



class Bgnd(Section, OdvObject):
	_section_name = "BGND"
	_section_version = 4

	def _load(self, substream: ReadStream) -> None:
		size = substream.read(UShort)
		self.dvm_filename = substream.read(String, size)
		self.minimap_image = substream.read(Image)

	def _save(self, substream: WriteStream) -> None:
		substream.write(UShort(len(self.dvm_filename)))
		substream.write(String(self.dvm_filename))
		substream.write(self.minimap_image)






