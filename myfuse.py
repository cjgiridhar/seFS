#############################################################################
# myfuse.py - Implementation of seFS
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
import errno
import fuse
import stat
import time
from seFS import seFS

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

fuse.fuse_python_api = (0, 2)

class Buffer: # {{{1

  """
  This class wraps cStringIO.StringIO with two additions: The __len__
  method and a dirty flag to determine whether a buffer has changed.
  """

  def __init__(self):
    self.buf = cStringIO.StringIO()
    self.dirty = False

  def __getattr__(self, attr, default=None):
    """ Delegate to the StringIO object. """
    return getattr(self.buf, attr, default)

  def __len__(self):
    """ Get the total size of the buffer in bytes. """
    position = self.buf.tell()
    self.buf.seek(0, os.SEEK_END)
    length = self.buf.tell()
    self.buf.seek(position, os.SEEK_SET)
    return length

  def truncate(self, *args):
    """ Truncate the file at the current position and set the dirty flag. """
    if len(self) > self.buf.tell():
      self.dirty = True
    return self.buf.truncate(*args)

  def write(self, *args):
    """ Write a string to the file and set the dirty flag. """
    self.dirty = True
    return self.buf.write(*args)


class MyFS(fuse.Fuse):
    def __init__(self, *args, **kw):
        fuse.Fuse.__init__(self, *args, **kw)

        # Set some options required by the Python FUSE binding.
        self.flags = 0
        self.multithreaded = 0

	self.fd = 0
	self.sefs = seFS()
	ret = self.sefs.open('/')
	print "Created root with %s" %ret
	self.sefs.write('/', "Root of the seFS")
	t = int(time.time())
	mytime = (t, t, t)
	ret = self.sefs.utime('/', mytime)
	print ret
	self.sefs.setinode('/', 1)
	self.is_dirty = False

    def getdir(self, path):
	print "in getdir"

    def getattr(self, path):
	sefs = seFS()
        st = fuse.Stat()
	c  = fuse.FuseGetContext()
	print c
	print "getattr called path= %s", path
	if path == '/':
        	st.st_nlink = 2
       		st.st_mode = stat.S_IFDIR | 0755
	else:
		print "For a regular file %s" %path
		st.st_mode = stat.S_IFREG | 0777
        	st.st_nlink = 1

	st.st_uid, st.st_gid = (c['uid'], c['gid'])

       	ret = sefs.search(path)
	print "From database getattr ret=", ret 
	if ret is True:
		tup = sefs.getutime(path)
		print tup
		st.st_mtime = int(tup[0].strip().split('.')[0])
		st.st_ctime = int(tup[1].strip().split('.')[0])
		st.st_atime = int(tup[2].strip().split('.')[0])

		st.st_ino    = int(sefs.getinode(path))
		print "inode = %d" %st.st_ino
		if sefs.getlength(path) is not None:
			st.st_size = int(sefs.getlength(path))
		else:
			st.st_size = 0
		return st
	else:
       		return - errno.ENOENT

    def readdir(self, path, offset):
	print "readdir", path
	yield fuse.Direntry('.')
        yield fuse.Direntry('..')

	sefs = seFS()
	all_files = sefs.ls()
	print "Rest of the files in root dir"
	print all_files

	for e in all_files:
		if str(e) == '/':
			continue
       		yield fuse.Direntry(str(e[1:]))

    def link(self, target_path, link_path, nested=False):
        print "In link****"

    def open(self, path, flags):
        print "open: trying to open %s"  %path
	sefs = seFS()
	ret = sefs.search(path)
	print ret
	if ret is True:
		return 0
	return -errno.ENOENT

    def truncate(self, length):
	print "In truncate"
	return 0

    def mkdir(self, path, mode):
	flags = None
	self.create(path, flags, mode| stat.S_IFDIR)
	return 0

    def create(self, path, flags=None, mode=None):
        print "trying to create %s", path
        print path
        print flags

	sefs = seFS()
	ret = self.open(path, flags)
	print ret

	if ret == -errno.ENOENT:
		# Create the file in database
		ret = sefs.open(path)
		print ret
		print "Creating the file %s" %path
		t = int(time.time())
		mytime = (t, t, t)
		ret = sefs.utime(path, mytime)
		print ret
		self.fd = len(sefs.ls())
		print "In create:fd = %d" %(self.fd)
		sefs.setinode(path, self.fd)
		print sefs.ls()
	else:
		print "The file %s exists!!" %path
	return 0

    def write(self, path, data, offset):
	print "In write path=%s" %path
	length = len(data)
	print "The data is %s len=%d offset=%d" %(str(data), length, offset)
	sefs = seFS()
	ret = sefs.write(path, data)
	return length

    def release(self, path, flags):
	print "In release"
	if self.is_dirty is True:
		print "Flushing buffer"
		print self.buf.read()
		sefs = seFS()
		ret = sefs.write(path, self.buf.read())
		print self.buf.read()
		#self.buf.close()
		#del self.buf
		self.is_dirty = False
		print ret
	return 0

    def readlink(self, path):
	print "In readlink"

    def link(self, target_path, link_path, nested=False):
	print "In link"

    def truncate(self, path, size):
	print "In truncate"

    def mknod (self, path, mode, dev):
	print "mknod called"
	return 0

    def access(self, path, flag):
        print "access path=%s" %path
	sefs = seFS()
	if sefs.search(path) is True:
		print "In access, found the file %s" %path
		return 0
	else:
		print "Could not find the file %s" %path
		return -errno.EACCES

    def read(self, path, size, offset):
	try:
		print "In read %s %d %d" %(path, size, offset)
		sefs = seFS()
		ret = sefs.read(path)
		print "read(): %s" %(ret)
		fbuf = StringIO()
		fbuf.write(str(ret))
		return fbuf.getvalue()
	except Exception, e:
		print "read failed"
		return e

    def chmod(self, path, mode):
	print "In chmod %s %s" %(path, str(mode))
        #self.files[path]['st_mode'] &= 0770000
        #self.files[path]['st_mode'] |= mode
        return 0

    def chown(self, path, uid, gid):
	print "In chown %s %d %d" %(path, uid, gid)
        #self.files[path]['st_uid'] = uid
	#self.files[path]['st_gid'] = gid
	return 0

    def utime(self, path, times=None):
	print "In utime %s" %(path)
	print times

	atime, mtime = times

	sefs = seFS()
	ret = sefs.utime(path, (atime, mtime, atime))

	print ret
	return 0

    def utimens(self, path, ts_acc, ts_mod):
	print "In utimens %s" %(path)
	print ts_acc, ts_mod
	atime = ts_acc.tv_sec + (ts_acc.tv_nsec / 1000000.0)
        mtime = ts_mod.tv_sec + (ts_mod.tv_nsec / 1000000.0)
	ctime = atime

	mytime = (mtime, ctime, atime)
	sefs = seFS()
	ret = sefs.utime(path, mytime)
	print ret

    def unlink(self,path):
	print "In unlink path %s" %path
	sefs = seFS()
	ret = sefs.remove(path)
	return

    def fgetattr(path, fh=None):
	print "In fgetattr"
	return 0

if __name__ == '__main__':
    fs = MyFS()
    fs.parse(errex=1)
    fs.main()
