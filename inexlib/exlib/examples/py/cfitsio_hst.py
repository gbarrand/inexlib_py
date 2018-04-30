# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

# Attempting to have the viewer in another process by using the multiprocessing module.

# Linux : ok.
# macOS : the ">>> cfitsio_hst._process.terminate()" stops the whole program.
# Windows : it does not work.

import inlib

cmap = inlib.SOPI_colrj32()

lut = inlib.lut_double(-0.04,0.4,cmap.size())

file = '../../../data/hst-img-2010x1890.fits'

import exlib

slice = 0
ihdu = 1;
img = inlib.img_byte();
yswap = False
if exlib.fits_image_read_slice_to_img(inlib.get_cout(),file,ihdu,slice,yswap,lut,cmap,img) == False :
  print('read_slice failed.')
else:
  print 'size ',img.size()

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
stop_thread = False

def vis_img(a_img,a_stop):
  if a_img.is_empty() == True : return;
  #//////////////////////////////////////////////////////////
  #/// create scene graph ///////////////////////////////////
  #//////////////////////////////////////////////////////////
  sep = inlib.sg_separator()
  sep.thisown = 0

  camera = inlib.sg_ortho()
  camera.thisown = 0
  camera.height.value(2)
  camera.znear.value(0.1)
  sep.add(camera)

  mat = inlib.sg_rgba()
  mat.thisown = 0
  mat.color.value(inlib.colorf_white())
  sep.add(mat)

  _img = inlib.sg_tex_rect()
  _img.thisown = 0
 #_img.img.value(a_img)
  _img.img.value().transfer(a_img)
  sep.add(_img)

  #//////////////////////////////////////////////////////////
  #/// visualize ////////////////////////////////////////////
  #//////////////////////////////////////////////////////////
  smgr = exlib.session(inlib.get_cout()) # screen manager
  if smgr.is_valid() == True :
    viewer = exlib.sg_viewer(smgr,0,0,700,500)
    if viewer.has_window() == True :
      viewer.sg().add(sep)
      viewer.show()
      print('steer...')
     #smgr.steer() # it blocks input from the prompt (because threading module is not a truely multi-thread system).
      import time
      while True:
        if a_stop() == True : break
        if smgr.sync() == False : break
        time.sleep(0.01)
      print('end steer.')
    del viewer
  del smgr

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////

import threading

_thread = threading.Thread(target=vis_img, args=(img,lambda: stop_thread))

print('stop viewer thread by closing the window or with : cfitsio_hst.stop_thread = True')

_thread.start()

del img


                
