#############################################################################
# SQLiteHandler.py - Class responsible for working with the SQlite databases.
#
# PyLibrary                      Version 1.0
# Copyright 2010 Chetan Giridhar cjgiridhar@gmail.com
# Created: 11/15/2010             Last Modified: 05/03/2012
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


import sqlite3,os

class SQLiteHandler:
	"""
		SQLiteHandler class is responsible for working with the SQlite databases.
		
		__init__() - Takes the path of the database as an argument. 
		connect() - Establishes a connection to the database.
		execute() - Executes the SQL queries on the database.
		commit() - This method commits the current transaction.
		close() - This closes the database connection.
	"""
	
	def __init__(self, databasepath):
		"""
			Gets the database location
		"""
		self.path = databasepath
		if not os.path.exists(self.path):
			raise Exception ("Database not found!")
		self.connection = None
		self.query = None
		
	def connect(self):
		"""
			Creates the connection object
		"""
		try:
			self.connection = sqlite3.connect(self.path)
			return self.connection
		except sqlite3.Error, msg:
			raise msg
	
	def execute(self,query):
		"""
			Executes SQL queries by creating the cursor object
		"""
		self.query = query
		try:
			self.cursorobj = self.connection.cursor()
			if self.cursorobj is not None:
				self.cursorobj.execute(self.query)
				return self.cursorobj
		except sqlite3.Error, msg:
			raise msg

	def fetchAll(self, query):
		"""
			Wrapper to fetch rows of select query output
		"""
		self.query = query
		row = self.connection.cursor().execute(self.query)
		self.commit()
		return row.fetchall()
		
	def fetchOne(self, query):
		"""
			Wrapper to fetch first row of select query output
		"""
		self.query = query
		row = self.connection.cursor().execute(self.query)
		self.commit()
		return row.fetchone()	

	def commit(self):
		"""
			Commits a transaction on DB
		"""
		try:
			if self.connection is not None:
				self.connection.commit()
		except sqlite3.Error, msg:
			raise msg
	
	def close(self):
		"""
			Closes the database connection
		"""
		try:
			if self.connection is not None:
				self.connection.close()
		except sqlite3.Error, msg:
			raise msg
			
			
if __name__ == '__main__':
	sql = SQLiteHandler('C:\\Python27\\testDB')
	sql.connect()
	row = sql.execute(''' insert into StudentInfo (name, marks) values ('Aniket', 99)''')
	sql.commit()
	row = sql.execute(''' insert into StudentInfo (name, marks) values ('Aniket', 99)''')
	sql.commit()
	print sql.fetchAll(''' select * from StudentInfo ''')
	print sql.fetchOne(''' select * from StudentInfo ''')
	sql.close()
