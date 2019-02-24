# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

#//////////////////////////////////////////////////////////
#/// args : ///////////////////////////////////////////////
#//////////////////////////////////////////////////////////
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-vis_mode', dest='vis_mode',required=False,help='Visualization mode')
parser.add_argument('-vis_host', dest='vis_host',required=False,help='host to display on')
parser.add_argument('-vis_port', dest='vis_port',required=False,help='port to display on')
args = parser.parse_args(None)

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////

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
  exit()

#print ('size ');print(img.size())

del cmap
del lut
  
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
stop_thread = False

def vis_img(a_img):
  if a_img.is_empty() == True : return
    
  #//////////////////////////////////////////////////////////
  #/// create scene graph ///////////////////////////////////
  #//////////////////////////////////////////////////////////
  all_sep = inlib.sg_separator()
  #all_sep.thisown = 0

  camera = inlib.sg_ortho()
  camera.thisown = 0
  camera.height.value(2)
  camera.znear.value(0.1)
  all_sep.add(camera)

  sep = inlib.sg_separator()
  #sep.thisown = 0  #decided below.
  #all_sep.add(sep) #decided below.
  
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
  width = 700
  height = 500
  
  if args.vis_mode == "offscreen" :
    import exlib_offscreen as exlib

    all_sep.add(sep)
    sep.thisown = 0
    gl2ps_mgr = exlib.sg_gl2ps_manager()
    zb_mgr = inlib.sg_zb_manager()
    factor = 2  # have greater size to have good freetype rendering.
    _width = factor*width
    _height = factor*height
    clear_color = inlib.colorf_white()
    file = 'out_cfitsio_hst_vis.ps'
    format = "INZB_PS"
    exlib.sg_write_paper(inlib.get_cout(),gl2ps_mgr,zb_mgr,\
                         clear_color.r(),clear_color.g(),clear_color.b(),clear_color.a(),\
                         all_sep,_width,_height,file,format)
    file = 'out_cfitsio_hst_vis.png'
    format = "INZB_PNG"
    exlib.sg_write_paper(inlib.get_cout(),gl2ps_mgr,zb_mgr,\
                         clear_color.r(),clear_color.g(),clear_color.b(),clear_color.a(),\
                         all_sep,_width,_height,file,format)
    del clear_color
    del all_sep     # before the below mgr.
    del zb_mgr
    del gl2ps_mgr

  elif args.vis_mode == "client" :
    del all_sep

    host = args.vis_host
    port = int(args.vis_port)
    #print("try to connected to "+host+" "+str(port)+" ...")
  
    import exlib_offscreen as exlib
    dc = exlib.net_sg_client(inlib.get_cout(),False,True)  #False=quiet, True=warn if receiving unknown protocol.
    if dc.initialize(host,port) == False:
      print("can't connect to "+host+" "+str(port))
      exit()

    if dc.send_string(inlib.sg_s_protocol_clear_static_sg()) == False:
      print("send protocol_s_rwc_clear_static_scene() failed.")
      exit()

    opts = inlib.args()
    opts.add(inlib.sg_s_send_placement(),inlib.sg_s_placement_static())
    if dc.send_sg(sep,opts) == False:
      print("send_sg failed.")
      exit()

    if dc.socket().send_string(inlib.sg_s_protocol_disconnect()) == False:
      print("send protocol_s_disconnect() failed.")
      exit()

    dc.socket().disconnect()
    del dc

    del sep
    
  else:
    print('exit viewer steering by closing the window with the mouse.')
    import exlib_window as exlib
    smgr = exlib.session(inlib.get_cout()) # screen manager
    if smgr.is_valid() == True :
      viewer = exlib.sg_viewer(smgr,0,0,width,height)
      if viewer.has_window() == True :
        all_sep.add(sep)
        sep.thisown = 0
        all_sep.thisown = 0
        viewer.sg().add(all_sep)
        viewer.show()
        smgr.steer()
      del viewer
    del smgr

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////

vis_img(img)

del img


                
