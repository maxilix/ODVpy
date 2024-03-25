#!/usr/bin/enc python3

import os

from PIL import Image

from c_stream import BytesStream
from settings import TRANSPARENT_GREEN, PaddingError

from common import *



class Frame():

	def __init__(self, stream):
		# Frame : 14 bytes
	
		self.sprite_id = stream.read(UShort)
		self.duration = stream.read(UShort)
		distance = stream.read(UShort)
		self.offset_x = stream.read(UShort)
		self.offset_y = stream.read(UShort)
		self.sound_effect = stream.read(UShort)
		stream.read(Padding, 2)




class Animation():

	def __init__(self, stream):
		# Animation : 54 bytes
		stream.read(Padding, 4)
		self.nb_frames = stream.read(UShort)
		unknown0 = stream.read(UShort)
		unknown1 = stream.read(UShort)
		coordonate_x = stream.read(UInt)
		coordonate_y = stream.read(UInt)
		self.persective = stream.read(UShort)
		self.id = stream.read(UShort)
		self.name = stream.read(String, 32)
		assert self.name[0] == "_"
		self.name = self.name[1:]
		self.frames = [Frame(stream) for _ in range(self.nb_frames)]


	def __repr__(self):
		return f"<Animation {self.name} ({self.id}-{self.persective}) {len(self.frames)} frame{("","s")[len(self.frames)>1]}>"


	def save(self, path, sprites):
		filename = f"{path}/{self.name}_{self.persective:02}.gif"

		min_offset_x = min([frame.offset_x for frame in self.frames ])
		min_offset_y = min([frame.offset_y for frame in self.frames ])
		total_width = max([frame.offset_x+sprites[frame.sprite_id].width for frame in self.frames ]) - min_offset_x
		total_height = max([frame.offset_y+sprites[frame.sprite_id].height for frame in self.frames ]) - min_offset_y

		bmp_frame = []
		for frame in self.frames:
			sprites[frame.sprite_id].build_bmp(total_width,total_height,frame.offset_x-min_offset_x, frame.offset_y-min_offset_y)
			for _ in range(max(1,frame.duration)):
				bmp_frame.append(sprites[frame.sprite_id].bmp)
		bmp_frame[0].save(filename, save_all=True, append_images=bmp_frame[1:], optimize=False, duration=100, loop=0)




class Profile():




	def __init__(self, stream):
		# Profile Header : 116 bytes
		self.name = stream.read_string()
		self.nb_perspectives = stream.read(UShort)
		stream.read_padding(32)
		self.nb_animations = stream.read(UShort)
		stream.read_padding(16)
		max_width = stream.read(UShort)
		max_height = stream.read(UShort)
		coordonate_x = stream.read(UInt)
		coordonate_y = stream.read(UInt)
		stream.read_padding(20)
		self.animations = [Animation(stream) for _ in range(self.nb_animations * self.nb_perspectives)]
		self._debug__check_animation_unicity()


	def _debug__check_animation_unicity(self):
		seen = set()
		for animation in self.animations:
			if (animation.id, animation.persective) in seen:
				print(f"WARNING : dual animation {animation.__repr__()}")
			seen.add((animation.id, animation.persective))


	def __getitem__(self, id):
		rop = [animation for animation in self.animations if animation.id == id]
		if rop == []:
			raise IndexError(f"no animation with id {id}")
		rop.sort(key=lambda a: a.persective)
		return rop


	def list_animations(self):
		for animation in self.animations:
			print(f"{animation.id:3}-{animation.persective:2} {animation.name}")


	def save(self, path, sprites):
		path = f"{path}/{self.name}"
		if not os.path.isdir(path):
			os.mkdir(path)
		for animation in self.animations:
			animation.save(path, sprites)





class Sprite(Pixmap, ReadableFromStream):


	@classmethod
	def from_stream(cls, stream):
		# Sprite Header : 10 bytes
		size = stream.read(UInt)
		width = stream.read(UShort)
		height = stream.read(UShort)
		stream.read(Padding, 2, pattern=b'\x01\x00')
		data = stream.read_bytes(size)
		return cls(width, height, data)

	def build(self, width_total=None, height_total=None, x_offset=0, y_offset=0):
		if width_total is None:
			width_total = self.width
		if height_total is None:
			height_total = self.height
		assert self.width+x_offset <= width_total
		assert self.height+y_offset <= height_total

		stream = BytesStream(self.data)

		self.bmp = Image.new('RGB', (width_total, height_total), color=TRANSPARENT_GREEN)
		for y in range(self.height):
			nb_transparent_pixel = stream.read(UShort)
			nb_total_pixel = stream.read(UShort)
			for x in range(self.width):
				if nb_total_pixel == 65535 or x > nb_total_pixel:
					break
				elif x < nb_transparent_pixel:
					continue
				else:
					pixel = stream.read(Pixel)
					self.bmp.putpixel((x+x_offset,y+y_offset), pixel.to_rgb())










class DvfParser():


z

	extension = "dvm"

	def __init__(self, filename):
		super().__init__(filename)

		self.version = stream.read(UShort)
		assert version == 512
		nb_sprites = stream.read(UShort)
		stream.read(Padding, 2)
		self.max_width = stream.read(UShort)
		self.max_height = stream.read(UShort)
		stream.read(Padding, 20)

		self.sprites = [stream.read(Sprite) for _ in range(nb_sprites)]

		nb_profiles = stream.read(UShort)
		self.profiles = [stream.read(Profile) for _ in range(nb_profiles)]


	def print_list_profiles(self):
		for index, profile in enumerate(self.profiles):
			print(f"{index:2} {profile.name}")


	def save(self):
		path = self.name
		if not os.path.isdir(path):
			os.mkdir(path)
		for profile in self.profiles:
			profile.save(path, self.sprites)





