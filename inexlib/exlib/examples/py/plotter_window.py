# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

import inlib

#//////////////////////////////////////////////////////////
#/// create and fill histogram : //////////////////////////
#//////////////////////////////////////////////////////////
h = inlib.histo_h1d('Rand gauss',100,-5,5)

rg = inlib.rgaussd(0,1)
for I in range(0,10000): h.fill(rg.shoot(),1)
del rg

#print(h.entries());print(h.mean());print(h.rms())

#//////////////////////////////////////////////////////////
#/// create and fill a 2D cloud : /////////////////////////
#//////////////////////////////////////////////////////////
c2 = inlib.histo_c2d('Rand gauss/BW')

rg = inlib.rgaussd(0,1)
rbw = inlib.rbwd(0,1)
for I in range(0,10000): c2.fill(rg.shoot(),rbw.shoot(),1)
del rg
del rbw

print(c2.entries());print(c2.mean_y());print(c2.rms_y())

#//////////////////////////////////////////////////////////
#/// plotting : ///////////////////////////////////////////
#//////////////////////////////////////////////////////////
import exlib_window as exlib

gl2ps_mgr = exlib.sg_gl2ps_manager()
smgr = exlib.session(inlib.get_cout()) # screen manager
if smgr.is_valid() == True :
  plotter = exlib.plotter(smgr,2,1,0,0,700,500)
  if plotter.has_window() == True :
    sgp = plotter.plots().current_plotter()
    sgp.bins_style(0).color.value(inlib.colorf_blue())
    sgp.infos_style().font.value(inlib.font_arialbd_ttf())
    sgp.infos_x_margin.value(0.01) #percent of plotter width.
    sgp.infos_y_margin.value(0.01) #percent of plotter height.

    plotter.plot(h)

    plotter.plots().next()
    sgp = plotter.plots().current_plotter()
    sgp.points_style(0).color.value(inlib.colorf_red())
    sgp.infos_style().font.value(inlib.font_arialbd_ttf())
    sgp.infos_x_margin.value(0.01) #percent of plotter width.
    sgp.infos_y_margin.value(0.01) #percent of plotter height.

    plotter.plot(c2)

    plotter.plots().view_border.value(False)

    waction = exlib.sg_gl2ps_action(gl2ps_mgr,inlib.get_cout(),plotter.width(),plotter.height())
    waction.open('out.ps')
    plotter.sg().render(waction)
    waction.close()
    del waction
    
    plotter.show()

    plotter.steer()

  del plotter

del smgr
del gl2ps_mgr
del h
del c2
                
