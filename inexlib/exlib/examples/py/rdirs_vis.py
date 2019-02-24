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
parser.add_argument('-vis_format', dest='vis_format',required=False,help='format for output')
parser.add_argument('-number_of_points', dest='number_of_points',required=False,help='number_of_points per cluster')
args = parser.parse_args(None)

if args.number_of_points == None :
  number_of_points = 100000
else:
  number_of_points = int(args.number_of_points)

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
import inlib
import math

rgd = inlib.rtausmed()
rdir = inlib.rdir3d()

xyz = inlib.std_vector_double()

#print("fill clouds ...")

c_1 = inlib.histo_c3d('xyz')
for i in range(0,number_of_points):
  r = rgd.shoot()
  rdir.shoot(xyz)
  c_1.fill(r*xyz[0],r*xyz[1],r*xyz[2],1)

c_2 = inlib.histo_c3d('xyz')
center = [3,0,0]
for i in range(0,number_of_points):
  r = rgd.shoot()
  rdir.shoot(xyz)
  c_2.fill(center[0]+r*2*xyz[0],center[1]+r*2*xyz[1],center[2]+r*0.5*xyz[2],1)

c_3 = inlib.histo_c3d('xyz')
center = [0,3,0]
for i in range(0,number_of_points):
  r = 1+0.5*rgd.shoot()
  rdir.shoot(xyz)
  c_3.fill(center[0]+r*0.5*xyz[0],center[1]+r*2*xyz[1],center[2]+r*2*xyz[2],1)

#//////////////////////////////////////////////////////////
#/// plotting : ///////////////////////////////////////////
#//////////////////////////////////////////////////////////
import exlib_window as exlib

#print("plotting ...")

def set_plotters(a_plotter,a_c_1,a_c_2,a_c_3):
  sgp = a_plotter.plots().current_plotter()
  sgp.shape.value(inlib.sg_plotter.xyz)
  sgp.shape_automated.value(False)
      
  sgp.infos_style().visible.value(False)
  #sgp.infos_style().font.value(inlib.font_arialbd_ttf())
  #sgp.infos_x_margin.value(0.01) #percent of plotter width.
  #sgp.infos_y_margin.value(0.01) #percent of plotter height.

  sgp.points_style(0).color.value(inlib.colorf_red())
 #sgp.points_style(0).modeling.value(inlib.modeling_markers())
 #sgp.points_style(0).marker_size.value(7)
 #sgp.points_style(0).marker_style.value(inlib.marker_dot)
 #sgp.points_style(0).marker_style.value(inlib.marker_cross)
  sgp.points_style(0).modeling.value(inlib.modeling_points())
  sgp.points_style(0).point_size.value(1)
 
  sgp.points_style(1).color.value(inlib.colorf_blue())
  sgp.points_style(1).marker_style.value(inlib.marker_dot)
 
  sgp.points_style(2).color.value(inlib.colorf_green())
  sgp.points_style(2).marker_style.value(inlib.marker_dot)
 
  box = inlib.box3f()
  box.extend_by(a_c_1.lower_edge_x(),a_c_1.lower_edge_y(),a_c_1.lower_edge_z())
  box.extend_by(a_c_1.upper_edge_x(),a_c_1.upper_edge_y(),a_c_1.upper_edge_z())
  box.extend_by(a_c_2.lower_edge_x(),a_c_2.lower_edge_y(),a_c_2.lower_edge_z())
  box.extend_by(a_c_2.upper_edge_x(),a_c_2.upper_edge_y(),a_c_2.upper_edge_z())
  box.extend_by(a_c_3.lower_edge_x(),a_c_3.lower_edge_y(),a_c_3.lower_edge_z())
  box.extend_by(a_c_3.upper_edge_x(),a_c_3.upper_edge_y(),a_c_3.upper_edge_z())
    
  sgp.x_axis_automated.value(False)
  sgp.x_axis_min.value(box.mn().x())
  sgp.x_axis_max.value(box.mx().x())
    
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(box.mn().y())
  sgp.y_axis_max.value(box.mx().y())
    
  sgp.z_axis_automated.value(False)
  sgp.z_axis_min.value(box.mn().z())
  sgp.z_axis_max.value(box.mx().z())
    
  a_plotter.plots().view_border.value(False)
    
if args.vis_mode == "offscreen" :
  #print("plot (offscreen) ...")
  import offscreen
  p = offscreen.plotter(inlib.get_cout(),1,1,400,400)
  set_plotters(p,c_1,c_2,c_3)
  if args.vis_format == "bsg":
    p.out_bsg('out_rdirs_vis.bsg')
  else:      
    p.write_paper('out_rdirs_vis.ps','INZB_PS')
    p.write_paper('out_rdirs_vis.png','INZB_PNG')
  del p

elif args.vis_mode == "client" :
  import inexlib_client
    
  style_file = "./res/ioda.style"
  p = inexlib_client.plotter(inlib.get_cout(),1,1,args.vis_host,int(args.vis_port),style_file)

  p.plot_cloud3D(c_1)
  p.plot_cloud3D(c_2)
  p.plot_cloud3D(c_3)

  set_plotters(p,c_1,c_2,c_3)

  #p.set_plotters_style("ROOT_default")
  if args.vis_host == "134.158.76.71":  #LAL/wallino.
    p.set_plotters_style("wall_ROOT_default")
  p.send_clear_static_scene()
  p.send_plots()
  del p

else:
  smgr = exlib.session(inlib.get_cout()) # screen manager
  if smgr.is_valid() == True :
    plotter = exlib.gui_plotter(smgr,1,1,0,0,700,500)
    if plotter.has_window() == True :
      plotter.plot(c_1)
      plotter.plot(c_2)
      plotter.plot(c_3)
      
      set_plotters(plotter,c_1,c_2,c_3)
      
      plotter.set_plane_viewer(False)
      plotter.set_scene_light_on(False)
      plotter.hide_main_menu()
      plotter.hide_meta_zone()
      plotter.show_camera_menu()
        
      plotter.show()
  
      plotter.steer()
  
    del plotter
  
  del smgr
  
del c_1
del c_2
del c_3
                
