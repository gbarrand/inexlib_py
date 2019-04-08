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
parser.add_argument('-number_of_points', dest='number_of_points',required=False,help='number_of_points for c3d')
args = parser.parse_args(None)

if args.number_of_points == None :
  number_of_points = 20000
else:
  number_of_points = int(args.number_of_points)

#//////////////////////////////////////////////////////////
#/// create a scene graph : ///////////////////////////////
#//////////////////////////////////////////////////////////
import inlib

rgd = inlib.rtausmed()

def add_rcube(a_vertices):
  a_vertices.add(rgd.shoot()-0.5,rgd.shoot()-0.5,rgd.shoot()-0.5)
  
def add_rcube_2(a_vertices):
  a_vertices.add(2*rgd.shoot()-1.0,rgd.shoot()-0.5,rgd.shoot()-0.5)
  
def create_all_sep(a_sep):
  all_sep = inlib.sg_separator()
  #all_sep.thisown = 0
  
  camera = inlib.sg_ortho()
  camera.thisown = 0
  camera.position.value(inlib.vec3f(0,0,5))
  camera.height.value(7)
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
  m.set_rotate(0,1,0,0.5)
  m.mul_translate(-0.5,2.5,0)
  all_sep.add(m)

  a_sep.thisown = 0
  all_sep.add(a_sep)
  
  return all_sep
  
#///////////////////////////////////////////////////
#///////////////////////////////////////////////////
#///////////////////////////////////////////////////
sep = inlib.sg_separator()
#sep.thisown = 0

_color = inlib.colorf_blue()
if args.vis_host == "134.158.76.71":  #LAL/wallino.
  _color = inlib.colorf_white()
_color.set_a(0.5)

#///////////////////////////////////////////////////
#/// two cubes blended : ///////////////////////////
#///////////////////////////////////////////////////
_sep = inlib.sg_separator()
_sep.thisown = 0
sep.add(_sep)

blend = inlib.sg_blend()
blend.thisown = 0
blend.on.value(True)
_sep.add(blend)

m = inlib.sg_matrix()
m.thisown = 0
m.set_translate(0,0,0)
_sep.add(m)

mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(_color)
_sep.add(mat)
  
rcube = inlib.sg_vertices()
rcube.thisown = 0
rcube.mode.value(inlib.points())
_sep.add(rcube)
[add_rcube(rcube) for i in range(0,number_of_points)]
  
mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(inlib.colorf_black())
_sep.add(mat)

ds = inlib.sg_draw_style()
ds.thisown = 0
ds.style.value(inlib.draw_lines)
#ds.line_width.value(1)
_sep.add(ds)

cube = inlib.sg_cube()
cube.thisown = 0
_sep.add(cube)

#///////////////////////////////////////////////////
#/////////////////////////////////////////////////_//
_sep = inlib.sg_separator()
_sep.thisown = 0
sep.add(_sep)

blend = inlib.sg_blend()
blend.thisown = 0
blend.on.value(True)
_sep.add(blend)

m = inlib.sg_matrix()
m.set_translate(1,0,0)
m.thisown = 0
_sep.add(m)

mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(_color)
_sep.add(mat)
  
rcube = inlib.sg_vertices()
rcube.thisown = 0
rcube.mode.value(inlib.points())
_sep.add(rcube)
[add_rcube(rcube) for i in range(0,number_of_points)]
  
mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(inlib.colorf_black())
_sep.add(mat)
  
ds = inlib.sg_draw_style()
ds.thisown = 0
ds.style.value(inlib.draw_lines)
_sep.add(ds)

cube = inlib.sg_cube()
cube.thisown = 0
_sep.add(cube)

#///////////////////////////////////////////////////
#/// two cubes not blended : ///////////////////////
#///////////////////////////////////////////////////
_sep = inlib.sg_separator()
_sep.thisown = 0
sep.add(_sep)

blend = inlib.sg_blend()
blend.thisown = 0
blend.on.value(False)
_sep.add(blend)

m = inlib.sg_matrix()
m.set_translate(0,-1.5,0)
m.thisown = 0
_sep.add(m)

mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(_color)
_sep.add(mat)
  
rcube = inlib.sg_vertices()
rcube.thisown = 0
rcube.mode.value(inlib.points())
_sep.add(rcube)
[add_rcube(rcube) for i in range(0,number_of_points)]
  
mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(inlib.colorf_black())
_sep.add(mat)
  
ds = inlib.sg_draw_style()
ds.thisown = 0
ds.style.value(inlib.draw_lines)
_sep.add(ds)

cube = inlib.sg_cube()
cube.thisown = 0
_sep.add(cube)

#///////////////////////////////////////////////////
#///////////////////////////////////////////////////
_sep = inlib.sg_separator()
_sep.thisown = 0
sep.add(_sep)

blend = inlib.sg_blend()
blend.thisown = 0
blend.on.value(False)
_sep.add(blend)

m = inlib.sg_matrix()
m.set_translate(1,-1.5,0)
m.thisown = 0
_sep.add(m)

mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(_color)
_sep.add(mat)
  
rcube = inlib.sg_vertices()
rcube.thisown = 0
rcube.mode.value(inlib.points())
_sep.add(rcube)
[add_rcube(rcube) for i in range(0,number_of_points)]
  
mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(inlib.colorf_black())
_sep.add(mat)
  
ds = inlib.sg_draw_style()
ds.thisown = 0
ds.style.value(inlib.draw_lines)
_sep.add(ds)

cube = inlib.sg_cube()
cube.thisown = 0
_sep.add(cube)

#///////////////////////////////////////////////////
#/// one elongated cube blended : //////////////////
#///////////////////////////////////////////////////
_sep = inlib.sg_separator()
_sep.thisown = 0
sep.add(_sep)

blend = inlib.sg_blend()
blend.thisown = 0
blend.on.value(True)
_sep.add(blend)

m = inlib.sg_matrix()
m.set_translate(0.5,-3,0)
m.thisown = 0
_sep.add(m)

mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(_color)
_sep.add(mat)
  
rcube = inlib.sg_vertices()
rcube.thisown = 0
rcube.mode.value(inlib.points())
_sep.add(rcube)
[add_rcube_2(rcube) for i in range(0,2*number_of_points)]

vec = rcube.xyzs.values()
lvec = len(vec)
vec_0 = []
vec_1 = []
for i in range(0,lvec,3):
  if vec[i] < 0:
    vec_0.append(vec[i])
    vec_0.append(vec[i+1])
    vec_0.append(vec[i+2])
  else:
    vec_1.append(vec[i])
    vec_1.append(vec[i+1])
    vec_1.append(vec[i+2])

mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(inlib.colorf_black())
_sep.add(mat)
  
ds = inlib.sg_draw_style()
ds.thisown = 0
ds.style.value(inlib.draw_lines)
_sep.add(ds)

cube = inlib.sg_cube()
cube.thisown = 0
cube.width.value(2.0)
_sep.add(cube)

#///////////////////////////////////////////////////
#/// elongated cube sorted in two and blended : ////
#///////////////////////////////////////////////////
_sep = inlib.sg_separator()
_sep.thisown = 0
sep.add(_sep)

blend = inlib.sg_blend()
blend.thisown = 0
blend.on.value(True)
_sep.add(blend)

m = inlib.sg_matrix()
m.set_translate(0.5,-4.5,0)
m.thisown = 0
_sep.add(m)

mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(_color)
_sep.add(mat)
  
rcube_0 = inlib.sg_vertices()
rcube_0.thisown = 0
rcube_0.mode.value(inlib.points())
_sep.add(rcube_0)
lvec_0 = len(vec_0)
for i in range(0,lvec_0,3):
  rcube_0.add(vec_0[i],vec_0[i+1],vec_0[i+2])
  
mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(inlib.colorf_orange())
_sep.add(mat)
  
rcube_1 = inlib.sg_vertices()
rcube_1.thisown = 0
rcube_1.mode.value(inlib.points())
_sep.add(rcube_1)
lvec_1 = len(vec_1)
for i in range(0,lvec_1,3):
  rcube_0.add(vec_1[i],vec_1[i+1],vec_1[i+2])
  
mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(inlib.colorf_black())
_sep.add(mat)
  
ds = inlib.sg_draw_style()
ds.thisown = 0
ds.style.value(inlib.draw_lines)
_sep.add(ds)

cube = inlib.sg_cube()
cube.thisown = 0
cube.width.value(2.0)
_sep.add(cube)

#///////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////

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
  file = 'out_two_cubes.ps'
  format = "INZB_PS"
  exlib.sg_write_paper(inlib.get_cout(),gl2ps_mgr,zb_mgr,\
                       clear_color.r(),clear_color.g(),clear_color.b(),clear_color.a(),\
                       all_sep,_width,_height,file,format)
  file = 'out_two_cubes.png'
  format = "INZB_PNG"
  exlib.sg_write_paper(inlib.get_cout(),gl2ps_mgr,zb_mgr,\
                       clear_color.r(),clear_color.g(),clear_color.b(),clear_color.a(),\
                       all_sep,_width,_height,file,format)
  del clear_color
  del zb_mgr
  del gl2ps_mgr
  del all_sep

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
  print('exit viewer steering by closing the window with the mouse.')
  import exlib_window as exlib
  smgr = exlib.session(inlib.get_cout())
  if smgr.is_valid() == True :
    viewer = exlib.sg_viewer(smgr,0,0,width,height)
    if viewer.has_window() == True :
      all_sep = create_all_sep(sep)
      all_sep.thisown = 0
      viewer.sg().add(all_sep)   # give ownership of all_sep to the viewer.
      viewer.show()
      smgr.steer() #FIXME : it blocks input from the prompt, why ?
    del viewer      
  del smgr
  
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
