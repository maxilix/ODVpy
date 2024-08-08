from PIL import Image

from settings import TRANSPARENT_GREEN

from common import *


class Frame(RStreamable):

    def __init__(self, sprite_id, duration, distance, offset, sound_id):
        self.sprite_id = sprite_id
        self.duration = duration
        self.distance = distance
        self.offset = offset
        self.sound_id = sound_id

    @classmethod
    def from_stream(cls, stream):
        sprite_id = stream.read(UShort)
        duration = stream.read(UShort)
        distance = stream.read(UShort)
        offset = (stream.read(UShort), stream.read(UShort))
        sound_id = stream.read(UShort)
        stream.read(Padding, 2)
        return cls(sprite_id, duration, distance, offset, sound_id)


class Animation(RStreamable):

    def __init__(self, coordinate_x, coordinate_y, perspective, id, name, frames):
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.perspective = perspective
        self.id = id
        self.name = name
        self.frames = frames

    @classmethod
    def from_stream(cls, stream):
        # Animation : 54 bytes
        stream.read(Padding, 4)
        nb_frames = stream.read(UShort)
        unknown0 = stream.read(UShort)
        unknown1 = stream.read(UShort)
        coordinate_x = stream.read(UInt)
        coordinate_y = stream.read(UInt)
        perspective = stream.read(UShort)
        id = stream.read(UShort)
        name = stream.read(String, 32)
        # assert self.name[0] == "_"
        # name = self.name[1:]
        frames = [stream.read(Frame) for _ in range(nb_frames)]

        return cls(coordinate_x, coordinate_y, perspective, id, name, frames)

    def __repr__(self):
        return f"<Animation {self.name} ({self.id}-{self.perspective}) {len(self.frames)} frame{("", "s")[len(self.frames) > 1]}>"

    # def save(self, path, sprites):
    #     filename = f"{path}/{self.name}_{self.perspective:02}.gif"
    #
    #     min_offset_x = min([frame.offset_x for frame in self.frames])
    #     min_offset_y = min([frame.offset_y for frame in self.frames])
    #     total_width = max([frame.offset_x + sprites[frame.sprite_id].width for frame in self.frames]) - min_offset_x
    #     total_height = max([frame.offset_y + sprites[frame.sprite_id].height for frame in self.frames]) - min_offset_y
    #
    #     bmp_frame = []
    #     for frame in self.frames:
    #         sprites[frame.sprite_id].build_bmp(total_width, total_height, frame.offset_x - min_offset_x,
    #                                            frame.offset_y - min_offset_y)
    #         for _ in range(max(1, frame.duration)):
    #             bmp_frame.append(sprites[frame.sprite_id].bmp)
    #     bmp_frame[0].save(filename, save_all=True, append_images=bmp_frame[1:], optimize=False, duration=100, loop=0)


class Profile(RStreamable):

    def __init__(self, name, max_width, max_height, coordinate_x, coordinate_y, animations):
        self.name = name
        self.max_width = max_width
        self.max_height = max_height
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.animations = animations

    @classmethod
    def from_stream(cls, stream):
        name = stream.read(String, 32)
        nb_perspectives = stream.read(UShort)
        stream.read(Padding, 32)
        nb_animations = stream.read(UShort)
        stream.read(Padding, 16)
        max_width = stream.read(UShort)
        max_height = stream.read(UShort)
        coordinate_x = stream.read(UInt)
        coordinate_y = stream.read(UInt)
        stream.read(Padding, 20)
        animations = [stream.read(Animation) for _ in range(nb_animations * nb_perspectives)]

        return cls(name, max_width, max_height, coordinate_x, coordinate_y, animations)

    # def _debug__check_animation_unicity(self):
    #     seen = set()
    #     for animation in self.animations:
    #         if (animation.id, animation.perspective) in seen:
    #             print(f"WARNING : dual animation {animation.__repr__()}")
    #         seen.add((animation.id, animation.perspective))

    def __getitem__(self, id):
        rop = [animation for animation in self.animations if animation.id == id]
        if rop == []:
            raise IndexError(f"no animation with id {id}")
        rop.sort(key=lambda a: a.persective)
        return rop

    def list_animations(self):
        for animation in self.animations:
            print(f"{animation.id:3}-{animation.perspective:2} {animation.name}")

    # def save(self, path, sprites):
    #     path = f"{path}/{self.name}"
    #     if not os.path.isdir(path):
    #         os.mkdir(path)
    #     for animation in self.animations:
    #         animation.save(path, sprites)


class Sprite(RStreamable):

    def __init__(self, width, height, data):
        self.width = width
        self.height = height
        self.data = data
        self.bmp = None

    @classmethod
    def from_stream(cls, stream):
        size = stream.read(UInt)
        width = stream.read(UShort)
        height = stream.read(UShort)
        stream.read(Padding, 2, pattern=b'\x01\x00')
        data = stream.read(Bytes, size)
        return cls(width, height, data)

    def build(self, width_total=None, height_total=None, x_offset=0, y_offset=0):
        if width_total is None:
            width_total = self.width
        if height_total is None:
            height_total = self.height
        assert self.width + x_offset <= width_total
        assert self.height + y_offset <= height_total

        stream = ReadStream(self.data)

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
                    self.bmp.putpixel((x + x_offset, y + y_offset), pixel.to_rgb())


class DvfParser(Parser):
    ext = "dvf"

    def __init__(self, filename):
        super().__init__(filename)

        version = self.stream.read(UShort)
        assert version == 512
        nb_sprites = self.stream.read(UShort)
        self.stream.read(Padding, 2)
        self.max_width = self.stream.read(UShort)
        self.max_height = self.stream.read(UShort)
        self.stream.read(Padding, 20)
        self.sprites = [self.stream.read(Sprite) for _ in range(nb_sprites)]

        nb_profiles = self.stream.read(UShort)
        self.profiles = [self.stream.read(Profile) for _ in range(nb_profiles)]

    def print_list_profiles(self):
        for index, profile in enumerate(self.profiles):
            print(f"{index:2} {profile.name}")

    # def save(self):
    #     path = self.abs_name
    #     if not os.path.isdir(path):
    #         os.mkdir(path)
    #     for profile in self.profiles:
    #         profile.save(path, self.sprites)
