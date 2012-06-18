
seFS - Storage Efficient File System based on Python-fuse bindings
--

seFS is a Python-FUSE based storage efficient file system that abstracts SQLite Database as a file system and provides storage efficiency with 
Data deduplication and compression. This is a prototype implementation and can be furthered scaled.
A project by:




Date Created: 6 June 2012



Setup:

1. Create a directory 
2. run myfuse.py to mount the directory created in Step 1
$./myfuse.py -f ./<dirpath>

Run:

Open another terminal and issue seFS supported commands like ls, ll, touch
$touch abc
$ll
$cat >> abc

Teardown:

You will need to unmount the directory using fuermount utility
$fusermount -u ./<dirpath>

Contact
--
Chetan Giridhar cjgiridhar@gmail.com

Vishal Kanaujia vishalkanaujia@gmail.com

License
--
GNU General Public License
Copyright