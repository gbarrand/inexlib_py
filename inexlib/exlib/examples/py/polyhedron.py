# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

import inlib
import exlib

def polyhedron():
  #//////////////////////////////////////////////////////////
  #/// create scene graph ///////////////////////////////////
  #//////////////////////////////////////////////////////////
  sep = inlib.sg_separator()
  sep.thisown = 0

  camera = inlib.sg_ortho()
  camera.thisown = 0
  camera.position.value(inlib.vec3f(0,0,5))
  camera.height.value(10)
  camera.znear.value(0.1)
  camera.zfar.value(100)
  sep.add(camera)

  light = inlib.sg_head_light()
  light.thisown = 0
  light.direction.value(inlib.vec3f(1,-1,-10))
 #light.on.value(False)
  sep.add(light)

  m = inlib.sg_matrix()
  m.thisown = 0
  m.set_rotate(0,1,0,inlib.fhalf_pi()/2)
  m.mul_rotate(1,0,0,inlib.fhalf_pi()/2)
  sep.add(m);

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
  smgr = exlib.session(inlib.get_cout()) # screen manager
  if smgr.is_valid() == True :
    viewer = exlib.sg_viewer(smgr,0,0,700,500)
    if viewer.has_window() == True :
      viewer.sg().add(sep)
      viewer.show()
      print('steer...')
      smgr.steer() #FIXME : it blocks input from the prompt, why ?
      print('end steer.')
    del viewer
  del smgr

print('exit viewer steering by closing the window with the mouse.')

polyhedron()  
