#############################################################################
# seFS.py - Database interface for seFS Database.
#
# seFS                            Version 1.0
# Copyright 2012 
# Chetan Giridhar cjgiridhar@gmail.com
# Vishal Kanaujia vishalkanaujia@gmail.com
# Created: 04/03/2012             Last Modified: 06/03/2012
#
# This file is part of seFS.
#
# seFS is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation; 
#
# seFS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#                                                                             
#############################################################################

from db.SQLiteHandler import SQLiteHandler
from security.Crypto import Crypto
from archive.Compression import Compression
import time,bz2, random,sys

class seFS:
	"""
		Class representing seFS
	"""
	def __init__(self):
		"""
			Connects to seFS database
		"""
		self.sql = SQLiteHandler('seFS')
		self.sql.connect()
		
	def ls(self):
		"""
			Implements ls operation
		"""
		rows = self.sql.execute(''' select * from file ''')
		list = []
		for row in rows:
			list.append(row[1])
		return list

	def getutime(self, path):
		"""
			Getter for utime
		"""
		rows = self.sql.execute(''' select mtime, ctime, atime from file where abspath='%s' ''' %( path))
		for row in rows:
			tup = (row[0], row[1], row[2])
			return tup

	def utime(self, path, times):
		"""
			Setter for utime
		"""
		print times
		mtime, ctime, atime = times
		print mtime, ctime, atime
		self.sql.execute(''' update file  set mtime='%s', ctime='%s', atime='%s' where abspath='%s' ''' %(mtime, ctime, atime, path))
		self.sql.commit()
		return times

	def setinode(self,path,inode):
		"""
			Setter for inode
		"""
		print path,inode
		self.sql.execute(''' update file  set inode = '%d' where abspath='%s' ''' %(inode, path))
		self.sql.commit()
		return inode

	def getinode(self,path):
		"""
			Getter for inode
		"""
		rows = self.sql.execute(''' select inode from file where abspath='%s' ''' %( path))
		for row in rows:
			return row[0]

	def getlength(self,path):
		"""
			Calculates length of data
		"""
		rows = self.sql.execute(''' select length from file where abspath='%s' ''' %( path))
		for row in rows:
			return row[0]

	def open(self, path):
		"""
			Implements file open() call
		"""
		self.sql.execute(''' insert into file (abspath) select '%s' where not exists (SELECT 1 FROM file WHERE abspath='%s') ''' %(path,path))
		self.sql.commit()
		return path
	
	def write(self, fh, data):
		"""
			Implements write() call
		"""
		length  = len(data)
		shaObj = Crypto(string = data)
		sha1 = shaObj.sha1()
		comp = Compression(data)
		compressed = comp.compress()
		rows = self.sql.execute(''' select id from fileinfo where sha='%s' ''' %(sha1) )
		id = None
		for row in rows:
			id = row[0]
		if id is None:
			self.sql.execute(''' insert into fileinfo (length, sha, compressed, data) values ('%s','%s','%s', '%s') ''' %(length, sha1, compressed, data))
			self.sql.commit()
			row = self.sql.execute(''' select id,length from fileinfo where sha='%s' ''' %(sha1))
			for rows in row:
				id = rows[0]
			print id,length
			self.sql.execute(''' update file set id='%d', length='%d' where abspath='%s' ''' %(id,length,fh))
			self.sql.commit()
			return
		else:
			self.sql.execute(''' update file set id='%d', length='%d' where abspath='%s' ''' %(id,length,fh))
			self.sql.commit()
			return
		
	def remove(self,abspath):
		"""
			Implements unlink() call
		"""
		self.sql.execute(''' delete from file where abspath='%s' ''' %(abspath))
		self.sql.commit()
		return
	
	def search(self, abspath):
		"""
			Search for database record
		"""
		rows = self.sql.execute(''' select * from file where abspath='%s' ''' %(abspath))
		if rows.fetchall():
			return True
		return False

	def read(self, fh):
		"""
			Implements read() call
		"""
		id  = None
		rows = self.sql.execute(''' select id from file where abspath='%s' ''' %(fh))
		for row in rows:
			id = row[0]

		if id is None:
			return None
		rows = self.sql.execute(''' select data from fileinfo where id='%d' ''' %id)
		for row in rows:
			return row[0]
		
		
	def __del__(self):
		"""
			Closes the databse connection
		"""
		self.sql.close()



