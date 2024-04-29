
class PaddingError(Exception):
	def __init__(self, message, padding):            
		super().__init__(message)
		self.padding = padding


class ReadingError(Exception):
	pass


class WritingError(Exception):
	pass


class NegativeUnsignedError(ValueError):
	pass


class TooBigError(ValueError):
	pass