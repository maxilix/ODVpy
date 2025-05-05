from typing import Self

from common import *
from ..odv_object import OdvObjectIterable, OdvObject
from .parser import Parser
from ..scb_native_names import OP_CODE_NAME


class ScbQuad(RWStreamable):
    op_code: UChar
    operand: bytes
    end: UChar

    def __str__(self):
        return f"{OP_CODE_NAME[self.op_code]}"

    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        rop = cls()
        rop.op_code = stream.read(UChar)
        # print(f"    {rop.op_code=}")
        rop.operand = stream.read(Bytes, 8)
        # print(f"    {rop.operand.hex()=}")
        rop.end = stream.read(UChar)
        assert rop.end == 126
        return rop

    def to_stream(self, stream: WriteStream) -> None:
        pass


class ScbFunction(OdvObject):
    function_name: str
    address: int
    nb_parameter: int
    ret_val_size: int
    parameter_size: int
    volatile_size: int
    tempor_size: int
    quad: list[ScbQuad] = []

    def __str__(self):
        return f"{self.function_name}"

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)
        assert "functionName " == stream.read(String, 13)
        rop.function_name = stream.read(String, end=" ")
        # print(f"    {rop.function_name=}")

        assert ", address " == stream.read(String, 10)
        rop.address = int(stream.read(String, end=","))
        # print(f"    {rop.address=}")

        assert " nbOfParams " == stream.read(String, 12)
        rop.nb_parameter = int(stream.read(String, end=","))
        # print(f"    {rop.nb_parameter=}")

        assert " sizeOfRetVal " == stream.read(String, 14)
        rop.ret_val_size = int(stream.read(String, end=","))
        # print(f"    {rop.ret_val_size=}")

        assert " sizeOfParams " == stream.read(String, 14)
        rop.parameter_size = int(stream.read(String, end="\n"))
        # print(f"    {rop.parameter_size=}")

        assert "functionParameters\n\n sizeOfVolatile " == stream.read(String, 36)
        rop.volatile_size = int(stream.read(String, end=","))
        # print(f"    {rop.volatile_size=}")

        assert " sizeOfTempor " == stream.read(String, 14)
        rop.tempor_size = int(stream.read(String, end="\n"))
        # print(f"    {rop.tempor_size=}")

        return rop


    def to_stream(self, stream: WriteStream) -> None:
        pass


class ScbClass(OdvObjectIterable):
    filename: str
    class_name: str
    nb_variable: int
    variable_size: int

    def __str__(self):
        return f"{self.class_name}"

    @classmethod
    def from_stream(cls, stream: ReadStream, *, parent) -> Self:
        rop = cls(parent)
        assert "fileName " == stream.read(String, 9)
        rop.filename = stream.read(String, end=" ")
        # print(f"  {rop.filename=}")
        assert ", className " == stream.read(String, 12)
        rop.class_name = stream.read(String, end="\n")
        # print(f"  {rop.class_name=}")
        assert "nbOfVariables " == stream.read(String, 14)
        rop.nb_variable = int(stream.read(String, end=","))
        # print(f"  {rop.nb_variable=}")
        assert " sizeOfVariables " == stream.read(String, 17)
        rop.variable_size = int(stream.read(String, end="\n"))
        # print(f"  {rop.variable_size=}")
        assert "nbOfFunctions " == stream.read(String, 14)
        nb_function = int(stream.read(String, end="\n"))
        # print(f"  {nb_function=}")

        for _ in range(nb_function):
            rop.add_child(stream.read(ScbFunction, parent=rop))

        assert "nbOfQuads " == stream.read(String, 10)
        nb_quad = int(stream.read(String, end="\n"))
        # print(f"  {nb_quad=}")

        addresses = [f.address for f in rop] + [nb_quad]
        for i in range(len(rop)):
            rop[i].quad = [stream.read(ScbQuad) for _ in range(addresses[i+1]-addresses[i])]

        return rop


    def to_stream(self, stream: WriteStream) -> None:
        pass





class ScbClassGroup(OdvObjectIterable):
    @classmethod
    def from_stream(cls, stream: ReadStream) -> Self:
        rop = cls()
        assert "nbOfClasses " == stream.read(String, 12)
        nb_class = int(stream.read(String, end="\n"))
        # print(f"{nb_class=}")
        for _ in range(nb_class):
            rop.add_child(stream.read(ScbClass, parent=rop))
        return rop



    def to_stream(self, stream: WriteStream) -> None:
        pass



class ScbParser(Parser):
    ext = "scb"

    def __init__(self, filename):
        super().__init__(filename)
        assert "version " == self.stream.read(String, 8)
        self.version = float(self.stream.read(String, end=","))
        # print(f"{self.version=}")
        assert " debug " == self.stream.read(String, 7)
        self.debug = bool(int(self.stream.read(String, end="\n")))
        # print(f"{self.debug=}")
        # self.classes = self.stream.read(ScbClassGroup)
        self.tail = self.stream.read_raw()


    def save_to_file(self, filename):
        stream = WriteStream()
        stream.write(String("version 1.00, debug 0\n"))
        stream.write(Bytes(self.tail))
        with open(filename, 'wb') as file:
            file.write(stream.get_value())
