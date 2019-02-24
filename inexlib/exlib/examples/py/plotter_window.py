# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

import inlib

number_of_points = 10000

verbose = False

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

if verbose == True : print("plot ...")

import exlib_window as exlib

smgr = exlib.session(inlib.get_cout()) # screen manager
if smgr.is_valid() == True :
  plotter = exlib.plotter(smgr,2,2,0,0,700,500)
  if plotter.has_window() == True :

    sgp = plotter.plots().current_plotter()
    sgp.bins_style(0).color.value(inlib.colorf_blue())
    sgp.infos_style().font.value(inlib.font_arialbd_ttf())
    sgp.infos_x_margin.value(0.01) #percent of plotter width.
    sgp.infos_y_margin.value(0.01) #percent of plotter height.
    sgp.plot(h)
    
    plotter.plots().next()
    sgp = plotter.plots().current_plotter()
    sgp.points_style(0).color.value(inlib.colorf_blue())
    sgp.points_style(0).modeling.value(inlib.modeling_points())
    sgp.infos_style().font.value(inlib.font_arialbd_ttf())
    sgp.infos_x_margin.value(0.01) #percent of plotter width.
    sgp.infos_y_margin.value(0.01) #percent of plotter height.
    sgp.plot(c2)
    
    plotter.plots().next()
    sgp = plotter.plots().current_plotter()
    sgp.shape.value(inlib.sg_plotter.xyz)
    sgp.shape_automated.value(False)
    sgp.points_style(0).color.value(inlib.colorf_blue())
    sgp.points_style(0).modeling.value(inlib.modeling_points())
    sgp.points_style(0).point_size.value(1)
    sgp.infos_style().font.value(inlib.font_arialbd_ttf())
    sgp.infos_x_margin.value(0.01) #percent of plotter width.
    sgp.infos_y_margin.value(0.01) #percent of plotter height.
    sgp.plot(c3)

    plotter.plots().view_border.value(False)

    plotter.show()

    plotter.steer()

  del plotter

del smgr

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
del h
del c2
del c3                
