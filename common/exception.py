
class PaddingError(Exception):
	def __init__(self, message, padding):            
		super().__init__(message)
		self.padding = padding


class ReadingTypeError(TypeError):
	pass


class WritingTypeError(TypeError):
	pass
