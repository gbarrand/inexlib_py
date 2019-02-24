# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

#//////////////////////////////////////////////////////////
#/// args : ///////////////////////////////////////////////
#//////////////////////////////////////////////////////////
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

verbose = False
if args.verbose == "True" : verbose = True

#////////////////////////////////////////////////////////////
#/// create and fill a 3D cloud with the csv file : /////////
#////////////////////////////////////////////////////////////
import inlib

c3 = inlib.histo_c3d('from csv')

import csv
file = open(file_name)
csv_reader = csv.reader(file, delimiter=',')
first_line = False
line_count = 0
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
      #print(row[0])
    else:
      c3.fill(float(row[0]),float(row[1]),float(row[2]),1)
  line_count += 1
  
file.close()

if verbose == True : 
  print("inlib::histo::c3d entries : "+str(c3.entries()))
  print("  mean x = "+str(c3.mean_x())+", rms x = "+str(c3.rms_x()))
  print("  mean y = "+str(c3.mean_y())+", rms y = "+str(c3.rms_y()))
  print("  mean z = "+str(c3.mean_z())+", rms z = "+str(c3.rms_z()))
  print("  low x = "+str(c3.lower_edge_x())+", up x = "+str(c3.upper_edge_x()))
  print("  low y = "+str(c3.lower_edge_y())+", up y = "+str(c3.upper_edge_y()))
  print("  low z = "+str(c3.lower_edge_z())+", up z = "+str(c3.upper_edge_z()))
  
#///////////////////////////////////////////////////////////////////////////////////////
#/// plotting : /////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////

if args.vis_mode == "window" :
  if verbose == True : print("plot (window) ...")
  import window
  p = window.plotter(inlib.get_cout(),1,1,0,0,700,500)
  p.plot_cloud3D(c3)
  p.show()
  p.steer()
  del p
    
elif args.vis_mode == "offscreen" :
  if verbose == True : print("plot (offscreen) ...")
  import offscreen
  p = offscreen.plotter(inlib.get_cout(),1,1,400,400)
  p.plot_cloud3D(c3)
  if args.vis_format == "bsg":
    p.out_bsg('out_csv_c3d_vis.bsg')
  else:
    p.write_paper('out_csv_c3d_vis.ps','INZB_PS')
    p.write_paper('out_csv_c3d_vis.png','INZB_PNG')
  del p

elif args.vis_mode == "client" :
  if verbose == True : print("plot (client) ...")

  import inexlib_client
    
  style_file = "./res/ioda.style"
  p = inexlib_client.plotter(inlib.get_cout(),1,1,args.vis_host,int(args.vis_port),style_file)

 #p.m_blend.on.value(True)
  sgp = p.plot_cloud3D(c3)
  color = inlib.colorf_blue()
  if args.vis_host == "134.158.76.71":  #LAL/wallino.
    color = inlib.colorf_white()
 #color = inlib.colorf_white() # on black background, it is nice
 #color.set_a(0.5)
  sgp.points_style(0).color.value(color)

  sgp.theta.value(0)
  sgp.phi.value(0)
  sgp.tau.value(0)

 #sgp.x_axis_automated.value(False)
 #sgp.x_axis_min.value(60.4)
 #sgp.x_axis_max.value(71)

 #sgp.y_axis_automated.value(False)
 #sgp.y_axis_min.value(-46.5)
 #sgp.y_axis_max.value(-32.9)

 #sgp.z_axis_automated.value(False)
 #sgp.z_axis_min.value(1.0)
 #sgp.z_axis_max.value(1.2)

 #p.set_plotters_style("ROOT_default")
 #if args.vis_host == "134.158.76.71":  #LAL/wallino.
 #  p.set_plotters_style("wall_ROOT_default")
  
  if verbose == True : print("send plots ...")
  
  p.send_clear_static_scene()
  p.send_plots()
  del p

else:
  if verbose == True : print("plot (gui_window) ...")
  import window
  p = window.gui_plotter(inlib.get_cout(),1,1,0,0,700,500)
  p.plot_cloud3D(c3)
  p.show()
  p.steer()
  del p

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
del c3                
