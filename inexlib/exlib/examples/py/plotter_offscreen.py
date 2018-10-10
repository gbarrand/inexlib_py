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
for I in range(0,500): c3.fill(rg.shoot(),rbw.shoot(),rg.shoot(),1)
del rg
del rbw

#//////////////////////////////////////////////////////////
#/// plotting : ///////////////////////////////////////////
#//////////////////////////////////////////////////////////
import exlib_offscreen as exlib

inlib.env_append_path('EXLIB_FONT_PATH','./res')    
inlib.env_append_path('EXLIB_FONT_PATH','../res')    

gl2ps_mgr = exlib.sg_gl2ps_manager()

#//////////////////////////////////////////////////////////
#/// scene graph : ////////////////////////////////////////
#//////////////////////////////////////////////////////////
sep = inlib.sg_separator()
sep.thisown = 0

camera = inlib.sg_ortho()
camera.thisown = 0
camera.height.value(1)
z = 10*1
camera.znear.value(0.1*z)
camera.zfar.value(10*z)  # 100*z induces problems with lego rendering.
camera.position.value(inlib.vec3f(0,0,z))
camera.orientation.value(inlib.rotf(inlib.vec3f(0,0,1),0))
camera.focal.value(z)
sep.add(camera)

ttf = exlib.sg_text_freetype()

plots = inlib.sg_plots(ttf)
plots.thisown = 0
plots.set_regions(2,2)
sep.add(plots)

#//////////////////////////////////////////////////////////
#/// plot : ///////////////////////////////////////////////
#//////////////////////////////////////////////////////////
sgp = plots.current_plotter()

sgp.bins_style(0).color.value(inlib.colorf_blue())
sgp.infos_style().font.value(inlib.font_arialbd_ttf())
sgp.infos_x_margin.value(0.01) #percent of plotter width.
sgp.infos_y_margin.value(0.01) #percent of plotter height.
#plottable = inlib.h1d2plot(h)
#plottable.thisown = 0
#sgp.add_plottable(plottable)
sgp.plot(h)

plots.next()
sgp = plots.current_plotter()
sgp.points_style(0).color.value(inlib.colorf_red())
sgp.infos_style().font.value(inlib.font_arialbd_ttf())
sgp.infos_x_margin.value(0.01) #percent of plotter width.
sgp.infos_y_margin.value(0.01) #percent of plotter height.
sgp.plot(c2)

plots.next()
sgp = plots.current_plotter()
sgp.shape.value(inlib.sg_plotter.xyz)
sgp.shape_automated.value(False)
sgp.points_style(0).color.value(inlib.colorf_red())
sgp.points_style(0).marker_size.value(7)
sgp.points_style(0).marker_style.value(inlib.marker_cross)
sgp.infos_style().font.value(inlib.font_arialbd_ttf())
sgp.infos_x_margin.value(0.01) #percent of plotter width.
sgp.infos_y_margin.value(0.01) #percent of plotter height.
sgp.plot(c3)

plots.view_border.value(False)

width = 400
height = 200

plots.adjust_size(width,height)

#//////////////////////////////////////////////////////////
#/// output : /////////////////////////////////////////////
#//////////////////////////////////////////////////////////

waction = exlib.sg_gl2ps_action(gl2ps_mgr,inlib.get_cout(),width,height)
waction.open('out.ps')
sep.render(waction)
waction.close()
del waction
    
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
del sep
del ttf
del gl2ps_mgr
del h
del c2
                
