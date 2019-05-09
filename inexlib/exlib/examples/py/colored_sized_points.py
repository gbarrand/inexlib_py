# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

#//////////////////////////////////////////////////////////
#/// args : ///////////////////////////////////////////////
#//////////////////////////////////////////////////////////
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-verbose', dest='verbose',required=False,help='verbosity')
parser.add_argument('-vis_mode', dest='vis_mode',required=False,help='Visualization mode')
parser.add_argument('-vis_host', dest='vis_host',required=False,help='host to display on')
parser.add_argument('-vis_port', dest='vis_port',required=False,help='port to display on')
parser.add_argument('-vis_format', dest='vis_format',required=False,help='format for output')
parser.add_argument('-number_of_points', dest='number_of_points',required=False,help='number_of_points')
args = parser.parse_args(None)

if args.number_of_points == None :
  number_of_points = 10
else:
  number_of_points = int(args.number_of_points)

#//////////////////////////////////////////////////////////
#/// create a scene graph : ///////////////////////////////
#//////////////////////////////////////////////////////////
import inlib

#///////////////////////////////////////////////////
#///////////////////////////////////////////////////
#///////////////////////////////////////////////////
all_sep = inlib.sg_separator()
  
camera = inlib.sg_ortho()
camera.thisown = 0
camera.position.value(inlib.vec3f(0,0,10))
camera.focal.value(10)
camera.height.value(2)
camera.znear.value(0.1)
camera.zfar.value(100)
all_sep.add(camera)

light = inlib.sg_head_light()
light.thisown = 0
light.direction.value(inlib.vec3f(1,-1,-10))
#light.on.value(False)
all_sep.add(light)

#///////////////////////////////////////////////////
#///////////////////////////////////////////////////
#///////////////////////////////////////////////////
sep = inlib.sg_separator()
#sep.thisown = 0

m = inlib.sg_matrix()
m.thisown = 0
m.set_translate(0,0,0)
sep.add(m)

vtxs = inlib.sg_colored_sized_points()
vtxs.thisown = 0
sep.add(vtxs)

_color = inlib.colorf_grey()
_size = 50
x = 0
y = 0
z = 0
vtxs.add(x,y,z,_color.r(),_color.g(),_color.b(),_color.a(),_size)
  
rgd = inlib.rtausmed()

_color = inlib.colorf_red()
_size = 10
for i in range(0,number_of_points):
  x = rgd.shoot()-0.5
  y = rgd.shoot()-0.5
  z = rgd.shoot()-0.5
  #print("point "+str(x)+" "+str(y)+str(z))
  vtxs.add(x,y,z,_color.r(),_color.g(),_color.b(),_color.a(),_size)

_color = inlib.colorf_green()
_size = 15
for i in range(0,number_of_points):
  x = rgd.shoot()-0.5
  y = rgd.shoot()-0.5
  z = rgd.shoot()-0.5
  vtxs.add(x,y,z,_color.r(),_color.g(),_color.b(),_color.a(),_size)

_color = inlib.colorf_blue()
_size = 20
for i in range(0,number_of_points):
  x = rgd.shoot()-0.5
  y = rgd.shoot()-0.5
  z = rgd.shoot()-0.5
  vtxs.add(x,y,z,_color.r(),_color.g(),_color.b(),_color.a(),_size)

vtxs.center()
  
#///////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////

width = 700
height = 500
  
if args.vis_mode == "offscreen" :
  import exlib_offscreen as exlib
  
  sep.thisown = 0
  all_sep.add(sep)
      
  gl2ps_mgr = exlib.sg_gl2ps_manager()
  zb_mgr = inlib.sg_zb_manager()
  factor = 2  # have greater size to have good freetype rendering.
  _width = factor*width
  _height = factor*height
  clear_color = inlib.colorf_white()
  file = 'out_colored_sized_points.ps'
  format = "INZB_PS"
  exlib.sg_write_paper(inlib.get_cout(),gl2ps_mgr,zb_mgr,\
                       clear_color.r(),clear_color.g(),clear_color.b(),clear_color.a(),\
                       all_sep,_width,_height,file,format)
  file = 'out_colored_sized_points.png'
  format = "INZB_PNG"
  exlib.sg_write_paper(inlib.get_cout(),gl2ps_mgr,zb_mgr,\
                       clear_color.r(),clear_color.g(),clear_color.b(),clear_color.a(),\
                       all_sep,_width,_height,file,format)
  del clear_color
  del zb_mgr
  del gl2ps_mgr
  del all_sep

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
    print("send protocol_clear_static_scene() failed.")
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
  import exlib_window as exlib
  smgr = exlib.session(inlib.get_cout())
  if smgr.is_valid() == True :
    viewer = exlib.gui_viewer_window(smgr,0,0,width,height)
    if viewer.has_window() == True :
      sep.thisown = 0
      all_sep.add(sep)
      all_sep.thisown = 0
      viewer.scene().add(all_sep)
      
      viewer.set_scene_camera(camera)
      viewer.set_scene_light(light)
      viewer.set_plane_viewer(False)
      #viewer.set_scene_light_on(True)
  
      viewer.hide_main_menu()
      viewer.hide_meta_zone()
      viewer.show_camera_menu()

      viewer.show()
      viewer.steer()
      
      viewer.show()
    del viewer      
  del smgr
  
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
