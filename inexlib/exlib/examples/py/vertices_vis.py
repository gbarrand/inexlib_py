# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

#////////////////////////////////////////////////////////////
#/// args : /////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-verbose', dest='verbose',required=False,help='verbosity')
parser.add_argument('-vis_mode', dest='vis_mode',required=False,help='Visualization mode')
parser.add_argument('-vis_host', dest='vis_host',required=False,help='host to display on')
parser.add_argument('-vis_port', dest='vis_port',required=False,help='port to display on')
parser.add_argument('-vis_format', dest='vis_format',required=False,help='format for output')
parser.add_argument('-number_of_points', dest='number_of_points',required=False,help='number_of_points for c3d')
args = parser.parse_args(None)

if args.number_of_points == None :
  number_of_points = 10000
else:
  number_of_points = int(args.number_of_points)

#////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
import inlib
  
all_sep = inlib.sg_separator()
#all_sep.thisown = 0
  
camera = inlib.sg_ortho()
camera.thisown = 0
camera.position.value(inlib.vec3f(0,0,5))
camera.height.value(2)
camera.znear.value(0.1)
camera.zfar.value(100)
all_sep.add(camera)

light = inlib.sg_head_light()
light.thisown = 0
light.direction.value(inlib.vec3f(1,-1,-10))
 #light.on.value(False)
all_sep.add(light)

m = inlib.sg_matrix()
m.thisown = 0
#  m.set_rotate(0,1,0,0.785)
all_sep.add(m)

#////////////////////////////////////////////////////////////
#/// create a scene graph : /////////////////////////////////
#////////////////////////////////////////////////////////////
import inlib

sep = inlib.sg_separator()

#blend = inlib.sg_blend()
#blend.thisown = 0
#blend.on.value(True)
#sep.add(blend)

m = inlib.sg_matrix()
m.thisown = 0
sep.add(m)

_color = inlib.colorf_red()

mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(_color)
sep.add(mat)
  
vtxs = inlib.sg_vertices()
vtxs.thisown = 0
vtxs.mode.value(inlib.points())
sep.add(vtxs)

rgd = inlib.rtausmed()

def fill():
  vtxs.add(rgd.shoot(),rgd.shoot(),rgd.shoot())

[fill() for i in range(0,number_of_points)]

vtxs.center()

#////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
width = 700
height = 500

if args.vis_mode == "window" :
  print('exit viewer steering by closing the window with the mouse.')
  import exlib_window as exlib
  smgr = exlib.session(inlib.get_cout()) # screen manager
  if smgr.is_valid() == True :
    viewer = exlib.sg_viewer(smgr,0,0,width,height)
    if viewer.has_window() == True :
      sep.thisown = 0
      all_sep.add(sep)
      all_sep.thisown = 0
      viewer.sg().add(all_sep)
      viewer.show()
      print('steer...')
      smgr.steer()
      print('end steer.')
    del viewer
  del smgr
    
elif args.vis_mode == "offscreen" :
  import exlib_offscreen as exlib
  
  sep.thisown = 0
  all_sep.add(sep)
  
  gl2ps_mgr = exlib.sg_gl2ps_manager()
  zb_mgr = inlib.sg_zb_manager()
  factor = 2  # have greater size to have good freetype rendering.
  _width = factor*width
  _height = factor*height
  clear_color = inlib.colorf_white()
  file = 'out_csv_vertices_vis.ps'
  format = "INZB_PS"
  exlib.sg_write_paper(inlib.get_cout(),gl2ps_mgr,zb_mgr,\
                       clear_color.r(),clear_color.g(),clear_color.b(),clear_color.a(),\
                       all_sep,_width,_height,file,format)
  file = 'out_csv_vertices_vis.png'
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
    print("send protocol_clear_static_scene() failed.")
    exit()

 #if dc.send_string(inlib.sg_s_protocol_set_background_white()) == False:
  if dc.send_string(inlib.sg_s_protocol_set_background_black()) == False:
    print("send protocol_set_background_black() failed.")
    exit()

  opts = inlib.args()
  opts.add(inlib.sg_s_send_placement(),inlib.sg_s_placement_static())
  if dc.send_sg(sep,opts) == False:
    print("send_sg failed.")
    exit()

 #if dc.send_string(inlib.sg_s_protocol_reset_camera()) == False:
 #  print("send protocol_reset_camera() failed.")
 #  exit()
    
  if dc.send_string(inlib.sg_s_protocol_view_all()) == False:
    print("send protocol_view_all() failed.")
    exit()
    
  if dc.send_string(inlib.sg_s_protocol_disable_anim()) == False:
    print("send protocol_disable_anim() failed.")
    exit()
    
  if dc.socket().send_string(inlib.sg_s_protocol_disconnect()) == False:
    print("send protocol_s_disconnect() failed.")
    exit()

  dc.socket().disconnect()
  del dc

  del sep
  
else:  #gui_window
  print('exit viewer steering by closing the window with the mouse.')
  import exlib_window as exlib
  smgr = exlib.session(inlib.get_cout()) # screen manager
  if smgr.is_valid() == True :
    viewer = exlib.gui_viewer_window(smgr,0,0,width,height)
    if viewer.has_window() == True :
      sep.thisown = 0
      all_sep.add(sep)
      all_sep.thisown = 0
      viewer.scene().add(all_sep);
      viewer.set_scene_camera(camera);
      viewer.set_scene_light(light);
      viewer.set_plane_viewer(False);
      viewer.set_scene_light_on(True);
  
      viewer.hide_main_menu();
      viewer.hide_meta_zone();
      viewer.show_camera_menu();

      viewer.show();
      viewer.steer();
      
    del viewer
  del smgr

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
