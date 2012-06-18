seFS - Storage Efficient File System based on Python-fuse bindings
--

seFS is a Python-FUSE based storage efficient file system that abstracts SQLite Database as a file system and provides storage efficiency with 
Data deduplication and compression. seFS was developed on Ubuntu 11.04

Usage
--
<pre>
Setup
- Create a directory
- run myfuse.py to mount the directory created
   $./myfuse.py -f ./dirpath

Run
- Open another terminal and issue seFS file system commands
   $touch abc
   $ll
   $cat >> abc

Teardown
- You will need to unmount the directory using fuermount utility
   $fusermount -u ./dirpath
</pre>


Dependencies
--
- Ubuntu 11.04
- SQLite Database
- python-Fuse bindings
- Python 2.6

Limitation
--

This is a prototype file system implementation and can be furthered scaled.

Contact
--
- Chetan Giridhar cjgiridhar@gmail.com
- Vishal Kanaujia vishalkanaujia@gmail.com

License
--
GNU General Public License v3.0

Copyright (c) Chetan Giridhar, Vishal Kanaujia 2012