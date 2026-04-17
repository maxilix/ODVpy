from .exception import PaddingError
from .rw_base import Bytes, UInt

# TODO move in other place
X_MAX_OFFICIAL = 2944
Y_MAX_OFFICIAL = 2368


class Version(UInt):
    pass



class Padding(Bytes):
    def __new__(cls, data: int | bytes):
        if isinstance(data, bytes):
            return super().__new__(cls, data)
        elif isinstance(data, int):
            return super().__new__(cls, b'\x00' * data)
        else:
            raise Exception("Padding must be described as a pattern of bytes or a length of zeros.")

    @classmethod
    def from_stream(cls, stream, length=None, *, pattern=None):
        padding = super().from_stream(stream, length)
        if pattern is None and padding != b'\x00' * length:
            raise PaddingError(f"zero padding expected instead of : {padding}", padding=padding)
        elif pattern is not None and padding != pattern:
            raise PaddingError(f"{pattern} padding expected instead of : {padding}", padding=padding)
        # stream.debug_comment(f"Padding {padding.hex()}")
        return padding

    def to_stream(self, stream):
        super().to_stream(stream)
