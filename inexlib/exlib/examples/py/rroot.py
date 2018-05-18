# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

import os.path

file = '../../../data/wroot.root'
if os.path.isfile(file) == False :
  file = './wroot.root'
  if os.path.isfile(file) == False :
    print 'file wroot.root not found.'
    exit()
    
import inlib

EXIT_FAILURE = 1
EXIT_SUCCESS = 0

def main():
  rfile = inlib.rroot_file(inlib.get_cout(),file,False) # wroot.root produced by inlib/examples/cpp/wroot.cpp.
  if rfile.is_open() == False :
    print "can't open ../../../data/wroot.root"
    return EXIT_FAILURE

  keys = rfile.dir().keys()
  print 'number of keys = ',keys.size()

#  ls = True
#  dump = True
#  inlib.rroot_read(inlib.get_cout(),rfile,keys,True,ls,dump,0)
#  return EXIT_SUCCESS

  dir = inlib.rroot_find_dir(rfile.dir(),'histo')
  if dir == None :
    print 'directory histo not found'
    return EXIT_FAILURE
    
  key = dir.find_key('rg')
  if key == None :
    print 'rg histo not found'
    return EXIT_FAILURE
    
  h = inlib.rroot_key_to_h1d(rfile,key)
  if h == None :
    print 'key rg is not a h1d.'
    return EXIT_FAILURE

  print h.mean(),h.rms()
  
  rfile.close()
  return EXIT_SUCCESS

main()
