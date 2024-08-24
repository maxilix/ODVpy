from common import Parser, WriteStream
from .ai import Ai
from .bond import Bond
from .buil import Buil
from .cart import Cart
from .dlgs import Dlgs
from .fxbk import Fxbk
from .jump import Jump
from .lift import Lift
from .mat import Mat
from .misc import Misc
from .bgnd import Bgnd
from .move import Move
from .msic import Msic
from .pat import Pat
from .scrp import Scrp
from .sght import Sght
from .mask import Mask
from .snd import Snd
from .ways import Ways
from .elem import Elem


class DvdParser(Parser):
    ext = "dvd"

    def __init__(self, filename):
        super().__init__(filename)

        # Must be read in order
        self._misc = self.stream.read(Misc)
        self._bgnd = self.stream.read(Bgnd)
        self._move = self.stream.read(Move)
        self._sght = self.stream.read(Sght)
        self._mask = self.stream.read(Mask)
        self._ways = self.stream.read(Ways)
        self._elem = self.stream.read(Elem)
        self._fxbk = self.stream.read(Fxbk)
        self._msic = self.stream.read(Msic)
        self._snd = self.stream.read(Snd)
        self._pat = self.stream.read(Pat)
        self._bond = self.stream.read(Bond)
        self._mat = self.stream.read(Mat)
        self._lift = self.stream.read(Lift)
        self._ai = self.stream.read(Ai)
        self._buil = self.stream.read(Buil)
        self._scrp = self.stream.read(Scrp)
        self._jump = self.stream.read(Jump)
        self._cart = self.stream.read(Cart)
        self._dlgs = self.stream.read(Dlgs)

    def save_to_file(self, filename):
        stream = WriteStream()
        stream.write(self._misc)
        stream.write(self._bgnd)
        stream.write(self._move)
        stream.write(self._sght)
        stream.write(self._mask)
        stream.write(self._ways)
        stream.write(self._elem)
        stream.write(self._fxbk)
        stream.write(self._msic)
        stream.write(self._snd)
        stream.write(self._pat)
        stream.write(self._bond)
        stream.write(self._mat)
        stream.write(self._lift)
        stream.write(self._ai)
        stream.write(self._buil)
        stream.write(self._scrp)
        stream.write(self._jump)
        stream.write(self._cart)
        stream.write(self._dlgs)

        with open(filename, 'wb') as file:
            file.write(stream.get_value())

    @property
    def misc(self):
        if self._misc.loaded is False:
            self._misc.load()
        return self._misc

    @property
    def bgnd(self):
        if self._bgnd.loaded is False:
            self._bgnd.load()
        return self._bgnd

    @property
    def move(self):
        if self._move.loaded is False:
            self._move.load()
        return self._move

    @property
    def sght(self):
        if self._sght.loaded is False:
            self._sght.load(move=self.move)
        return self._sght

    @property
    def mask(self):
        if self._mask.loaded is False:
            self._mask.load()
        return self._mask

    @property
    def ways(self):
        if self._ways.loaded is False:
            self._ways.load()
        return self._ways

    @property
    def elem(self):
        if self._elem.loaded is False:
            self._elem.load()
        return self._elem

    @property
    def fxbk(self):
        if self._fxbk.loaded is False:
            self._fxbk.load()
        return self._fxbk

    @property
    def msic(self):
        if self._msic.loaded is False:
            self._msic.load()
        return self._msic

    @property
    def snd(self):
        if self._snd.loaded is False:
            self._snd.load()
        return self._snd

    @property
    def pat(self):
        if self._pat.loaded is False:
            self._pat.load()
        return self._pat

    @property
    def bond(self):
        if self._bond.loaded is False:
            self._bond.load(move=self.move, sght=self.sght)
        return self._bond

    @property
    def mat(self):
        if self._mat.loaded is False:
            self._mat.load()
        return self._mat

    @property
    def lift(self):
        if self._lift.loaded is False:
            self._lift.load(move=self.move)
        return self._lift

    @property
    def ai(self):
        if self._ai.loaded is False:
            self._ai.load()
        return self._ai

    @property
    def buil(self):
        if self._buil.loaded is False:
            self._buil.load(move=self.move)
        return self._buil

    @property
    def scrp(self):
        if self._scrp.loaded is False:
            self._scrp.load()
        return self._scrp

    @property
    def jump(self):
        if self._jump.loaded is False:
            self._jump.load(move=self.move)
        return self._jump

    @property
    def cart(self):
        if self._cart.loaded is False:
            self._cart.load()
        return self._cart

    @property
    def dlgs(self):
        if self._dlgs.loaded is False:
            self._dlgs.load()
        return self._dlgs
