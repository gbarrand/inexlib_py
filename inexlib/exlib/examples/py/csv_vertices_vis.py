# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

#////////////////////////////////////////////////////////////
#/// args : /////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-verbose', dest='verbose',required=False,help='verbosity')
parser.add_argument('-file', dest='file_name',required=True,help='Path to a data file')
parser.add_argument('-vis_mode', dest='vis_mode',required=False,help='Visualization mode')
parser.add_argument('-vis_host', dest='vis_host',required=False,help='host to display on')
parser.add_argument('-vis_port', dest='vis_port',required=False,help='port to display on')
parser.add_argument('-vis_format', dest='vis_format',required=False,help='format for output')
args = parser.parse_args(None)

file_name = args.file_name

#////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
def create_all_sep(a_sep):
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

  a_sep.thisown = 0
  all_sep.add(a_sep)
  
  return all_sep
  
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

#_color = inlib.colorf_red()
#if args.vis_host == "134.158.76.71":  #LAL/wallino.
#  _color = inlib.colorf_white()
#_color.set_a(0.5)

#mat = inlib.sg_rgba()
#mat.thisown = 0
#mat.color.value(_color)
#sep.add(mat)
  
vtxs = inlib.sg_atb_vertices()
#vtxs = inlib.sg_vertices()
vtxs.thisown = 0
vtxs.mode.value(inlib.points())
sep.add(vtxs)

#cmap = inlib.SOPI_midas_idl14()
cmap = inlib.SOPI_midas_heat()
cmap_size = cmap.size()

redshift_min = 1.0
redshift_max = 1.2
redshift_delta = redshift_max-redshift_min
#////////////////////////////////////////////////////////////
#/// add data to sg_vertices() //////////////////////////////
#////////////////////////////////////////////////////////////
import csv
file = open(file_name)
csv_reader = csv.reader(file, delimiter=',')
first_line = False
line_count = 0
num_items = 0
redshift_index = 2  # csv files with (ra,dec,redshift)
for row in csv_reader:
  if 0 <= line_count : 
 #if 0 <= line_count and line_count < 180000 :
 #if 0 <= line_count and line_count < 360000 :
 #if 0 <= line_count and line_count < 540000 :
 #if 60000 <= line_count and line_count < 120000 :
 #if 120000 <= line_count and line_count < 180000 :
 #if 180000 <= line_count and line_count < 360000 :
 #if 360000 <= line_count and line_count < 540000 :
 #if 540000 <= line_count and line_count < 720000 :
    if first_line == False:
      first_line = True
      num_items = len(row)
      #print("num_items = "+str(num_items))
      #print(row[0])
      if num_items < 3 :
        print("expect num columns >= 3.")
        exit(0)
      if num_items >=4 : redshift_index = 3 # csv file with (pos_x,pos_y,pos_z,redshift)
    else:
      color_factor = (float(row[redshift_index])-redshift_min)/redshift_delta
      #r = _color.r()*color_factor
      #g = _color.g()*color_factor
      #b = _color.b()*color_factor
      #a = 1
     #icolor = int(color_factor*(cmap_size-1))
      icolor = int((1.0-color_factor)*(cmap_size-1))
      SOPI_color = cmap.get_color(icolor)  # with midas_heat : icolor 0 is black, size-1 is white.
      r = SOPI_color.r()
      g = SOPI_color.g()
      b = SOPI_color.b()
      a = 1
     #vtxs.add(float(row[0]),float(row[1]),float(row[2]))
      vtxs.add_pos_color(float(row[0]),float(row[1]),float(row[2]),r,g,b,a)
  line_count += 1
  
file.close()
vtxs.center()

#////////////////////////////////////////////////////////////
#/// plotting : /////////////////////////////////////////////
#////////////////////////////////////////////////////////////
width = 700
height = 500

if args.vis_mode == "offscreen" :
  import exlib_offscreen as exlib
  all_sep = create_all_sep(sep)
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
      all_sep = create_all_sep(sep)
      all_sep.thisown = 0
      viewer.sg().add(all_sep)
      viewer.show()
      print('steer...')
      smgr.steer()
      print('end steer.')
    del viewer
  del smgr

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
