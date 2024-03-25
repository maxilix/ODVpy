#!/usr/bin/enc python3
"""
00 MISC
01 BGND
02 MOVE
03 SGHT
04 MASK
05 WAYS
06 ELEM
07 FXBK
08 MSIC
09 SND_
10 PAT_
11 BOND
12 MAT_
13 LIFT
14 AI__
15 BUIL
16 SCRP
17 JUMP
18 CART
19 DLGS
"""

import logging as log
from abc import ABC, abstractmethod


from common import *


# 20 dvd sections in order
section_list = ["MISC", "BGND", "MOVE", "SGHT", "MASK", "WAYS", "ELEM", "FXBK", "MSIC", "SND_", "PAT_", "BOND", "MAT_", "LIFT", "AI__", "BUIL", "SCRP", "JUMP", "CART", "DLGS"]


class Section(ReadableFromStream):

	def __init__(self, data):
		self.data = data
		log.info(f"Section {self.section} initialized.")

	@classmethod
	def from_stream(cls, stream):
		read_section = stream.read(String, 4)
		assert read_section == cls.section
		size = stream.read(UInt)
		data = stream.read(Bytes, size)
		return cls(data)

	def build(self, stream_rest):
		next_byte = stream_rest.read(Bytes, 1)
		assert next_byte == b''
		log.info(f"Section {self.section} builded.")