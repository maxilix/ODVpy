from config import Config
from odv.common import *
from odv.odv_object import OdvObject
from odv.section import Section


class Bgnd(Section, OdvObject):
	_section_id = 1
	_section_version = 4

	dvm_filename: String
	minimap_image: Image
	custom_dvm: bool
	complete_dvm_filename: Path
	map_image: Image

	def _load(self, substream: ReadStream, level:'Level') -> None:
		size = substream.read(UShort)
		self.dvm_filename = substream.read(String, size).lower()
		self.minimap_image = substream.read(Image)

		self.custom_dvm = False
		self.complete_dvm_filename = (level.base_path.parent / self.dvm_filename).with_suffix(".dvm")
		if not self.complete_dvm_filename.exists():
			if (index:=guess_level_index(self.dvm_filename)) != -1:
				self.complete_dvm_filename = original_filename(index, Config.backup_path).with_suffix(".dvm")
				print("[Section BGNG] Original DVM load from BGND dvm filename.")
				if level.index == -1:
					level.index = index
					print("[Section BGNG] Level index guessed from BGND dvm filename.")
			elif level.index != -1:
				self.complete_dvm_filename = original_filename(level.index, Config.backup_path).with_suffix(".dvm")
				print("[Section BGNG] Original DVM load from the guessed level index.")
			else:
				self.custom_dvm = True
				raise Exception(f"DVM cannot be load; Invalid Level index.")
		dvm_stream = ReadStream.from_file(self.complete_dvm_filename)
		self.map_image = dvm_stream.read(Image)

	def _save(self, substream: WriteStream) -> None:
		substream.write(UShort(len(self.dvm_filename)))
		substream.write(String(self.dvm_filename))
		substream.write(self.minimap_image)
