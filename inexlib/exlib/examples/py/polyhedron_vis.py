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
args = parser.parse_args(None)

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
import inlib
import exlib_window as exlib

def polyhedron():
  #//////////////////////////////////////////////////////////
  #/// create scene graph ///////////////////////////////////
  #//////////////////////////////////////////////////////////
  all_sep = inlib.sg_separator()
  #all_sep.thisown = 0  # decided below

  camera = inlib.sg_ortho()
  camera.thisown = 0
  camera.position.value(inlib.vec3f(0,0,5))
  camera.height.value(10)
  camera.znear.value(0.1)
  camera.zfar.value(100)
  all_sep.add(camera)

  light = inlib.sg_head_light()
  light.thisown = 0
  light.direction.value(inlib.vec3f(1,-1,-10))
 #light.on.value(False)
  all_sep.add(light)

  sep = inlib.sg_separator()
  #all_sep.add(sep)  # decided below
  #sep.thisown = 0  # decided below
  
  m = inlib.sg_matrix()
  m.thisown = 0
  m.set_rotate(0,1,0,inlib.fhalf_pi()/2)
  m.mul_rotate(1,0,0,inlib.fhalf_pi()/2)
  sep.add(m)

  mat = inlib.sg_rgba()
  mat.thisown = 0
  mat.color.value(inlib.colorf_green())
  sep.add(mat)

  # A Tube with a transvers hole :
  tubs_1 = inlib.hep_polyhedron_tubs(0.7,1.5,2,0,inlib.two_pi())
  tubs_2 = inlib.hep_polyhedron_tubs(  0,0.5,4,0,inlib.two_pi())
  tubs_2.Transform(inlib.rotd(inlib.vec3d(0,1,0),inlib.half_pi()),inlib.vec3d(0,0,0))
  op = tubs_1.subtract(tubs_2)

  node = inlib.sg_polyhedron()
  node.thisown = 0
 #node.ph.value(inlib.hep_polyhedron_sphere(0.9,1,0,inlib.two_pi(),0,inlib.pi()))
  node.ph.value(op)
 #node.solid.value(False)
 #node.reduced_wire_frame.value(False)
  sep.add(node)

  #//////////////////////////////////////////////////////////
  #/// viewing : ////////////////////////////////////////////
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
    file = 'out_polyhedron_vis.ps'
    format = "INZB_PS"
    exlib.sg_write_paper(inlib.get_cout(),gl2ps_mgr,zb_mgr,\
                         clear_color.r(),clear_color.g(),clear_color.b(),clear_color.a(),\
                         all_sep,_width,_height,file,format)
    file = 'out_polyhedron_vis.png'
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
    all_sep.add(sep)
    sep.thisown = 0
    smgr = exlib.session(inlib.get_cout())
    if smgr.is_valid() == True :
      viewer = exlib.sg_viewer(smgr,0,0,width,height)
      if viewer.has_window() == True :
        all_sep.thisown = 0
        viewer.sg().add(all_sep)   # give ownership of sep to the viewer.
        viewer.show()
        print('steer...')
        smgr.steer() #FIXME : it blocks input from the prompt, why ?
        print('end steer.')
      del viewer      
    del smgr
  
polyhedron()  

#format = 'GL2PS_EPS'
#format = "GL2PS_PS"
#format = "GL2PS_PDF"
#format = "GL2PS_SVG"
#format = "GL2PS_TEX"
#format = "GL2PS_PGF"
#format = "INZB_PS"
#format = "INZB_JPEG"
#format = "INZB_PNG"
