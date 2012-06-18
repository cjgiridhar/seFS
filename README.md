################################################
seFS - Storage Efficient File System based on Python-fuse bindings
------------------------------------

A project by:


Chetan Giridhar cjgiridhar@gmail.com

Vishal Kanaujia vishalkanaujia@gmail.com

Date Created: 6 June 2012

License: GNU General Public License

################################################

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