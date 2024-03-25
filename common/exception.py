#!/usr/bin/enc python3


class PaddingError(Exception):
	def __init__(self, message, padding):            
		super().__init__(message)
		self.padding = padding
