# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

import os.path

file = '../../data/hst-img-2010x1890.fits'
if os.path.isfile(file) == False :
  file = './data/hst-img-2010x1890.fits'
  if os.path.isfile(file) == False :
    file = './hst-img-2010x1890.fits'
    if os.path.isfile(file) == False :
      print('file hst-img-2010x1890.fits not found.')
      exit()
    
import inlib

cmap = inlib.SOPI_colrj32()

lut = inlib.lut_double(-0.04,0.4,cmap.size())

import exlib_window as exlib

slice = 0
ihdu = 1
img = inlib.img_byte()
yswap = False
if exlib.fits_image_read_slice_to_img(inlib.get_cout(),file,ihdu,slice,yswap,lut,cmap,img) == False :
  print('read_slice failed.')
else:
  print('size ');print(img.size())

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
stop_thread = False

def vis_img(a_img):
  if a_img.is_empty() == True : return
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
      smgr.steer()
      print('end steer.')
    del viewer
  del smgr

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////

import multiprocessing
_process = multiprocessing.Process(target=vis_img, args=(img,))

print('stop viewer process by closing the window or with >>> cfitsio_hst_mp._process.terminate()')

_process.start()

del img


                
