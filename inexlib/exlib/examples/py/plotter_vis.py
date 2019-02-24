# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

import inlib

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
  number_of_points = 10000
else:
  number_of_points = int(args.number_of_points)

verbose = False
if args.verbose == "True" : verbose = True

#//////////////////////////////////////////////////////////
#/// create and fill histogram : //////////////////////////
#//////////////////////////////////////////////////////////
h = inlib.histo_h1d('Rand gauss',100,-5,5)

rg = inlib.rgaussd(0,1)
for I in range(0,10000): h.fill(rg.shoot(),1)
del rg

#print h.entries(),h.mean(),h.rms()

#//////////////////////////////////////////////////////////
#/// create and fill a 2D cloud : /////////////////////////
#//////////////////////////////////////////////////////////
c2 = inlib.histo_c2d('Rand gauss/BW')

rg = inlib.rgaussd(0,1)
rbw = inlib.rbwd(0,1)
for I in range(0,10000): c2.fill(rg.shoot(),rbw.shoot(),1)
del rg
del rbw

#print c2.entries(),c2.mean_y(),c2.rms_y()

#//////////////////////////////////////////////////////////
#/// create and fill a 3D cloud : /////////////////////////
#//////////////////////////////////////////////////////////
c3 = inlib.histo_c3d('Rand gauss/BW/gauss')

rg = inlib.rgaussd(0,1)
rbw = inlib.rbwd(0,1)
for I in range(0,number_of_points): c3.fill(rg.shoot(),rbw.shoot(),rg.shoot(),1)
del rg
del rbw

if verbose == True :
  print("inlib::histo::c3d entries : "+str(c3.entries()))
  print("  mean x = "+str(c3.mean_x())+", rms x = "+str(c3.rms_x()))
  print("  mean y = "+str(c3.mean_y())+", rms y = "+str(c3.rms_y()))
  print("  mean z = "+str(c3.mean_z())+", rms z = "+str(c3.rms_z()))
  
#///////////////////////////////////////////////////////////////////////////////////////
#/// plotting : /////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////

if args.vis_mode == "window" :
  if verbose == True : print("plot (window) ...")
  import window
  p = window.plotter(inlib.get_cout(),2,2,0,0,700,500)
  p.plot_histo(h)
  p.next()
  p.plot_cloud2D(c2)
  p.next()
  p.plot_cloud3D(c3)
  p.show()
  p.steer()
  del p
    
elif args.vis_mode == "offscreen" :
  if verbose == True : print("plot (offscreen) ...")
  import offscreen
  p = offscreen.plotter(inlib.get_cout(),2,2,400,400)
  p.plot_histo(h)
  p.next()
  p.plot_cloud2D(c2)
  p.next()
  p.plot_cloud3D(c3)
  if args.vis_format == "bsg":
    p.out_bsg('out_plotter_vis.bsg')
  else:      
    p.write_paper('out_plotter_vis.ps','INZB_PS')
    p.write_paper('out_plotter_vis.png','INZB_PNG')
    
  del p

elif args.vis_mode == "client" :
  if verbose == True : print("plot (client) ...")

  import inexlib_client
    
  style_file = "./res/ioda.style"
  p = inexlib_client.plotter(inlib.get_cout(),2,2,args.vis_host,int(args.vis_port),style_file)
  p.plot_histo(h)
  p.next()
  p.plot_cloud2D(c2)
  p.next()
  p.plot_cloud3D(c3)

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
  p = window.gui_plotter(inlib.get_cout(),2,2,0,0,700,500)
  p.plot_histo(h)
  p.next()
  p.plot_cloud2D(c2)
  p.next()
  p.plot_cloud3D(c3)
  p.show()
  p.steer()
  del p
  
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
del h
del c2
del c3                
