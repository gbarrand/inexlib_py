# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

import inlib

#//////////////////////////////////////////////////////////
#/// create and fill histogram : //////////////////////////
#//////////////////////////////////////////////////////////
h = inlib.histo_h1d('Rand gauss',100,-5,5)

r = inlib.rgaussd(0,1)
for I in range(0,10000): h.fill(r.shoot(),1)
del r

#print h.entries(),h.mean(),h.rms()

#//////////////////////////////////////////////////////////
#/// plotting : ///////////////////////////////////////////
#//////////////////////////////////////////////////////////
import exlib_window as exlib

stop_thread = False

def plot_histo(a_h,a_stop):
  
  gl2ps_mgr = exlib.sg_gl2ps_manager()
  smgr = exlib.session(inlib.get_cout()) # screen manager
  if smgr.is_valid() == True :
    plotter = exlib.plotter(smgr,1,1,0,0,700,500)
    if plotter.has_window() == True :
      sgp = plotter.plots().current_plotter()
      sgp.bins_style(0).color.value(inlib.colorf_blue())
   
      sgp.infos_style().font.value(inlib.font_arialbd_ttf())
  
      sgp.infos_x_margin.value(0.01) #percent of plotter width.
      sgp.infos_y_margin.value(0.01) #percent of plotter height.
  
      plotter.plot_cp(a_h)
  
      plotter.plots().view_border.value(False)
  
      waction = exlib.sg_gl2ps_action(gl2ps_mgr,inlib.get_cout(),plotter.width(),plotter.height())
      waction.open('out.ps')
      plotter.sg().render(waction)
      waction.close()
      del waction
      
      plotter.show()
  
      print('steer...')
     #smgr.steer() # it blocks input from the prompt (because threading module is not a truely thread system).
      import time
      while True:
        if a_stop() == True : break
        if smgr.sync() == False : break
        time.sleep(0.01)

      print('end steer.')
  
    del plotter
  
  del smgr
  del gl2ps_mgr

import threading

_thread = threading.Thread(target=plot_histo, args=(h,lambda: stop_thread))

print('stop viewer thread by closing the window or with : plotter_thread.stop_thread = True')

_thread.start()

del h


                
