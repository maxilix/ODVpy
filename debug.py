
from common import *

import sys
from types import ModuleType, FunctionType
from gc import get_referents


X_MAX = 2944
Y_MAX = 2368

# Custom objects know their class.
# Function objects seem to know way too much, including modules.
# Exclude modules as well.
BLACKLIST = type, ModuleType, FunctionType


def size_of(obj):
	"""sum size of object & members."""
	if isinstance(obj, BLACKLIST):
		raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
	seen_ids = set()
	size = 0
	objects = [obj]
	while objects:
		need_referents = []
		for obj in objects:
			if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
				seen_ids.add(id(obj))
				size += sys.getsizeof(obj)
				need_referents.append(obj)
		objects = get_referents(*need_referents)
	return size


def cmp_obj_size(sprites):
	rop = []
	for sprite in sprites:
		size_before = size_of(sprite)
		sprite.build_bmp()
		size_after = size_of(sprite)
		rop.append((size_after-size_before)/size_before*100)
		print(f"{size_before} -> {size_after} \t {rop[-1]:.2f}%")
	print(f"\naverage : {sum(rop)/len(rop):.2f}%")


def print_level_map_size():
	for level in LEVEL:
		dvm = DvmParser(level.dvm)
		w = dvm.level_map.width
		h = dvm.level_map.height
		wb = w.to_bytes(2, 'little') 
		hb = h.to_bytes(2, 'little') 
		print(f"L{level.index:02} {wb.hex()} ({w}) x {hb.hex()} ({h})")


def hs_to_i(hex_string):
	if hex_string == "":
		return 0
	else:
		return int(hex_string[:2], 16) + hs_to_i(hex_string[2:])*256


def i_to_hsi(integer):
	if integer == 0:
		return "00"
	rop = hex(integer).lstrip("0x")
	if len(rop)%2==1:
		rop = "0"+rop
	#print(rop)
	rop = "".join(reversed([rop[i]+rop[i+1] for i in range(0,len(rop), 2)]))
	if integer > 9:
		rop += f" ({integer})"
	return rop


def search_coor(stream, limit):
	rop = []

	a = stream.read(UChar)
	b = stream.read(UChar)
	c = stream.read(UChar)
	d = stream.read(UChar)

	while True:
		if (x := b * 256 + a) < X_MAX and (y := d * 256 + c) < Y_MAX:
			rop.append(Coordinate(x, y))
		a, b, c, d = b, c, d, stream.read(UChar)
		if stream.tell() >= limit:
			break
	return rop