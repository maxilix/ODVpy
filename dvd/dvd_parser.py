#!/usr/bin/enc python3


import logging

from PIL import Image

from common import *
from .section import Section, section_list
from .misc import Miscellaneous
from .bgnd import MiniMap
from .move import Motion
from .sght import Sight
from .mask import Masks


class DvdParser(Parser):

	extension = "dvd"

	def __init__(self, filename):
		super().__init__(filename)

		self.misc = self.stream.read(Miscellaneous)
		self.bgnd = self.stream.read(MiniMap)
		self.move = self.stream.read(Motion)
		self.sght = self.stream.read(Sight)
		self.mask = self.stream.read(Masks)

		#self.build()

	def build(self):
		self.misc.build()
		self.bgnd.build()
		self.move.build()
		# self.sght.build()
		self.mask.build()
		pass





"""
def print_all_misc():

	misc_list = []
	for level_id in range(26):
		stream = ByteStream.from_file(f"./dvd_original_file/level_{level_id:02}.dvd")
		misc_list.append(DVD.Miscellaneous(stream))

	for misc in misc_list:
		print(misc.data.hex())


def print_sections(level_id):
	stream = ByteStream.from_file(f"./dvd_original_file/level_{level_id:02}.dvd")
	while True:
		section = stream.read_string(4)
		if section == "":
			break
		size = stream.read_uint()
		stream.read_bytes(size)
		print(f"{section} {size}")

print_all_misc()
"""