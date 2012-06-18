#############################################################################
# Crypto.py - Class responsible for 
# 1. calculating signatures for files and strings.
# 2. Represents hex and binary digests
#
# PyLibrary                      Version 1.0
# Copyright 2010 Chetan Giridhar cjgiridhar@gmail.com
# Created: 12/19/2010             Last Modified: 12/19/2010
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

import hashlib,os,base64,hmac

class Crypto:
	""" 
	Crypto class is responsible for calculating file signatures.
	
	__init__() - Takes the following as arguments.
		Filepath or string to be hashed
		Encoding format in which result to be displayed (hex, binary, base64)
		
	- md5() - Returns MD5 hash of file or string in specified format.
	- sha1() - Returns SHA1 hash of file or string in specified format.
	- sha224() - Returns SHA224 hash of file or string in specified format.
	- sha256() - Returns SHA256 hash of file or string in specified format.
	- sha384() - Returns SHA384 hash of file or string in specified format.
	- sha512() - Returns SHA512 hash of file or string in specified format.
	- hmac_md5() - Returns hmac_md5 hash of file or string in specified format.
	- hmac_sha1(() - Returns hmac_sha1 hash of file or string in specified format.
	
	"""
	
	def __init__(self, filepath = None, string = None, format = 'hex'):
		self.filepath = filepath
		self.string = string
		self.format = format
		self.isFile = None
		self.isString = None
		
		if self.filepath and self.string is None:
			raise "Either a string or a filepath should be present"
			
		if self.string is not None:
			self.isString = True			
			try:
				if type(self.string) is str:
					pass
			except Exception,msg:
				raise
		if self.filepath is not None:
			self.isFile = True
			try:
				self.fileobj = file(self.filepath, 'rb')
			except Exception,msg:
				raise

	def __encodedString(self, hash):
		if self.format is 'hex':
			return hash.hexdigest()
		if self.format is 'binary':
			return hash.digest()
		if self.format is 'base64':
			digest = hash.digest()
			return base64.encodestring(digest)
	
	def md5(self):
		md5 = hashlib.md5()
		if self.isString:
			md5.update(self.string)
		if self.isFile:
			while True:
				data = self.fileobj.read(10)
				if not data:
					break
				md5.update(data)
		return self.__encodedString(md5)	
			
	def sha1(self):
		sha1 = hashlib.sha1()
		if self.isString:
			sha1.update(self.string)
		if self.isFile:
			while True:
				data = self.fileobj.read(10)
				if not data:
					break
				sha1.update(data)
		return self.__encodedString(sha1)	

	def sha224(self):
		sha224 = hashlib.sha224()
		if self.isString:
			sha224.update(self.string)
		if self.isFile:
			while True:
				data = self.fileobj.read(10)
				if not data:
					break
				sha224.update(data)
		return self.__encodedString(sha224)	

	def sha256(self):
		try:
			fileobj = file(self.filepath, 'rb')
		except Exception,msg:
			raise
		sha256 = hashlib.sha256()
		while True:
			data = fileobj.read(10)
			if not data:
				break
			sha256.update(data)
		return sha256.hexdigest()		
		
	def sha384(self):
		sha384 = hashlib.sha384()
		if self.isString:
			sha384.update(self.string)
		if self.isFile:
			while True:
				data = self.fileobj.read(10)
				if not data:
					break
				sha384.update(data)
		return self.__encodedString(sha384)	
		
	def sha512(self):
		sha512 = hashlib.sha512()
		if self.isString:
			sha512.update(self.string)
		if self.isFile:
			while True:
				data = self.fileobj.read(10)
				if not data:
					break
				sha512.update(data)
		return self.__encodedString(sha512)	
		
		
	def hmac_md5(self, secretkey):
		hmac_md5 = hmac.new(secretkey)
		if self.isString:
			hmac_md5.update(self.string)
		if self.isFile:
			while True:
				data = self.fileobj.read(10)
				if not data:
					break
				hmac_md5.update(data)
		return self.__encodedString(hmac_md5)	

	def hmac_sha1(self, secretkey):
		hmac_sha1 = hmac.new(secretkey)
		if self.isString:
			hmac_sha1.update(self.string)
		if self.isFile:
			while True:
				data = self.fileobj.read(10)
				if not data:
					break
				hmac_sha1.update(data)
		return self.__encodedString(hmac_sha1)
	

if __name__ == '__main()__':
	hashObj1 = Crypto(string = 'This is a test string', format = 'base64')
	hashObj2 = Crypto(filepath = "C:\\Windows\\notepad.exe",  format = 'hex')
	hashObj3 = Crypto(format = 'hex') ## Throws an error as there is no filepath or string mentioned
	print hashObj1.md5()
	print hashObj1.hmac_sha1('its a secert')
	