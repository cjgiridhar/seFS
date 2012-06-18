#############################################################################
# Compression.py - Class responsible for compression of strings
#
# PyLibrary                      Version 1.0
# Copyright 2010 Chetan Giridhar cjgiridhar@gmail.com
# Created: 03/05/2010             Last Modified: 05/03/2012
#
# This file is part of PyLibrary.
#
# PyLibrary is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation; 
#
# PyLibrary is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#                                                                             
#############################################################################


import random
class Compression:
	"""
		 Class responsible for compression of strings
		 compress() - Compresses a string
		 decode() - Decodes the compression
	"""

	def __init__(self, string):
	    """
	    	Gets the string
	    """
	    self.string = string

	def decode(self):
	    """
	    	Decodes the compression
	    """
	    return 0

	def compress(self):
	    """ 
	    	Compresses the string
	    """
	    return self

comp = Compression('this is data')
print comp.compress()
