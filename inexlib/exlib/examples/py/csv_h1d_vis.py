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

center_ra = 62
half_ra = 0.9

ra_min = center_ra-half_ra
ra_max = center_ra+half_ra

ra_min = 60.4612922668
ra_max = 70.3106460571

#center_dec = -38.6
#center_dec = -38.5
center_dec = -38
half_dec = 0.01

dec_min = center_dec-half_dec
dec_max = center_dec+half_dec

z_min = 1
z_max = 1.04

y_max = 100
dec_step = -0.1
nbin = 100

if verbose == True : 
  print(ra_min)
  print(ra_max)
  print(dec_min)
  print(dec_max)

h1_0 = inlib.histo_h1d('0',nbin,ra_min,ra_max)
h1_1 = inlib.histo_h1d('1',nbin,ra_min,ra_max)
h1_2 = inlib.histo_h1d('2',nbin,ra_min,ra_max)
h1_3 = inlib.histo_h1d('3',nbin,ra_min,ra_max)

import csv
file = open(file_name)
csv_reader = csv.reader(file, delimiter=',')
first_line = False
for row in csv_reader:
  if first_line == False:
    first_line = True
    #print(row[0])
  else:
    ra = float(row[0])
    dec = float(row[1])
    z = float(row[2])
    _dec_min = dec_min
    _dec_max = dec_max
    if ra_min < ra and ra < ra_max and _dec_min < dec and dec < _dec_max and z_min < z and z < z_max: h1_0.fill(ra,1)
    _dec_min += dec_step
    _dec_max += dec_step
    if ra_min < ra and ra < ra_max and _dec_min < dec and dec < _dec_max and z_min < z and z < z_max: h1_1.fill(ra,1)
    _dec_min += dec_step
    _dec_max += dec_step
    if ra_min < ra and ra < ra_max and _dec_min < dec and dec < _dec_max and z_min < z and z < z_max: h1_2.fill(ra,1)
    _dec_min += dec_step
    _dec_max += dec_step
    if ra_min < ra and ra < ra_max and _dec_min < dec and dec < _dec_max and z_min < z and z < z_max: h1_3.fill(ra,1)
 
file.close()

if verbose == True : 
  print("inlib::histo::c3d entries : "+str(c3.entries()))
  print("  mean x = "+str(c3.mean_x())+", rms x = "+str(c3.rms_x()))
  print("  mean y = "+str(c3.mean_y())+", rms y = "+str(c3.rms_y()))
  print("  mean z = "+str(c3.mean_z())+", rms z = "+str(c3.rms_z()))
  
#///////////////////////////////////////////////////////////////////////////////////////
#/// plotting : /////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////
width = 700
height = 500

if args.vis_mode == "window" :
  if verbose == True : print("plot (window) ...")
  import window
  p = window.plotter(inlib.get_cout(),2,2,0,0,width,height)

  sgp = p.plot_histo(h1_0)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)
  p.next()
  sgp = p.plot_histo(h1_1)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)
  p.next()
  sgp = p.plot_histo(h1_2)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)
  p.next()
  sgp = p.plot_histo(h1_3)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)

  p.show()
  p.steer()
  del p
    
elif args.vis_mode == "offscreen" :
  if verbose == True : print("plot (offscreen) ...")
  import offscreen
  p = offscreen.plotter(inlib.get_cout(),2,2,width,height)
  
  sgp = p.plot_histo(h1_0)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)
  p.next()
  sgp = p.plot_histo(h1_1)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)
  p.next()
  sgp = p.plot_histo(h1_2)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)
  p.next()
  sgp = p.plot_histo(h1_3)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)

  if args.vis_format == "bsg":
    p.out_bsg('out_csv_h1d_vis.bsg')
  else:      
    p.write_paper('out_csv_h1d_vis.ps','INZB_PS')
    p.write_paper('out_csv_h1d_vis.png','INZB_PNG')
    
  del p

elif args.vis_mode == "client" :
  if verbose == True : print("plot (client) ...")

  import inexlib_client
    
  style_file = "./res/ioda.style"
  p = inexlib_client.plotter(inlib.get_cout(),2,2,args.vis_host,int(args.vis_port),style_file)
  sgp = p.plot_histo(h1_0)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)
  p.next()
  sgp = p.plot_histo(h1_1)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)
  p.next()
  sgp = p.plot_histo(h1_2)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)
  p.next()
  sgp = p.plot_histo(h1_3)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)

  #p.set_plotters_style("ROOT_default")
  if args.vis_host == "134.158.76.71":  #LAL/wallino.
    p.set_plotters_style("wall_ROOT_default")
  
  if verbose == True : print("send plots ...")
  
  p.send_clear_static_scene()
  p.send_plots()
  del p

else:
  if verbose == True : print("plot (gui_window) ...")
  import window
  p = window.gui_plotter(inlib.get_cout(),2,2,0,0,width,height)

  sgp = p.plot_histo(h1_0)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)
  p.next()
  sgp = p.plot_histo(h1_1)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)
  p.next()
  sgp = p.plot_histo(h1_2)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)
  p.next()
  sgp = p.plot_histo(h1_3)
  sgp.y_axis_automated.value(False)
  sgp.y_axis_min.value(0)
  sgp.y_axis_max.value(y_max)

  p.show()
  p.steer()
  
  del p
  
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
del h1_0
del h1_1
del h1_2
del h1_3
