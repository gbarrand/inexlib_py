// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

//exlib_build_use Python inlib inlib_glutess freetype GL gl2ps thread exlib
//exlib_build_use cfitsio
//exlib_build_use screen
//exlib_build_cppfile ../../exlib/spy/inlib_swig_py.cpp ../../exlib/spy/exlib_swig_py.cpp

#include <exlib/Python>

extern "C" {
  void initinlib_swig_py();
  void initexlib_swig_py();
}

#include <inlib/mem>
#include <inlib/system>

#include <inlib/S_STRING>
INLIB_GLOBAL_STRING(PYTHONHOME)
INLIB_GLOBAL_STRING(PYTHONPATH)

#include <string>
#include <iostream>

int main(int,char**) {
#ifdef INLIB_MEM
  inlib::mem::set_check_by_class(true);{
#endif

#ifdef ourex_Python_h
  if(!inlib::is_env(s_PYTHONHOME())) {
    inlib::putenv(s_PYTHONHOME(),"../../../ourex/Python");
  }
#endif
  inlib::putenv(s_PYTHONPATH(),"../../exlib/spy"); //to find [in,ex]lib.py.

  if(!::Py_IsInitialized()) ::Py_Initialize();
  ::PyEval_InitThreads();

  ::PyRun_SimpleString((char*)"print 'hello plotter_py_X11'");

  initinlib_swig_py();
  initexlib_swig_py();

  std::string s = "\n\
import inlib\n\
\n\
#//////////////////////////////////////////////////////////\n\
#/// create and fill histogram : //////////////////////////\n\
#//////////////////////////////////////////////////////////\n\
h = inlib.histo_h1d('Rand gauss',100,-5,5)\n\
\n\
r = inlib.rgaussd(0,1)\n\
for I in range(0,10000):\n\
  h.fill(r.shoot(),1)\n\
\n\
#print h.entries(),h.mean(),h.rms()\n\
\n\
#//////////////////////////////////////////////////////////\n\
#/// plotting : ///////////////////////////////////////////\n\
#//////////////////////////////////////////////////////////\n\
import exlib\n\
\n\
gl2ps_mgr = exlib.sg_gl2ps_manager()\n\
smgr = exlib.session(inlib.get_cout()) # screen manager\n\
if smgr.is_valid() == True :\n\
  plotter = exlib.plotter(smgr,1,1,0,0,700,500)\n\
  if plotter.has_window() == True :\n\
    sgp = plotter.plots().current_plotter()\n\
    sgp.bins_style(0).color.value(inlib.colorf_blue())\n\
 \n\
    inlib.env_append_path('EXLIB_FONT_PATH','.')    \n\
    inlib.env_append_path('EXLIB_FONT_PATH','..')    \n\
    sgp.infos_style().font.value(inlib.font_arialbd_ttf())\n\
\n\
    sgp.infos_x_margin.value(0.01) #percent of plotter width.\n\
    sgp.infos_y_margin.value(0.01) #percent of plotter height.\n\
\n\
    plotter.plot(h)\n\
\n\
    plotter.plots().view_border.value(False)\n\
\n\
    waction = exlib.sg_gl2ps_action(gl2ps_mgr,inlib.get_cout(),plotter.width(),plotter.height())\n\
    waction.open('out.ps')\n\
    plotter.sg().render(waction)\n\
    waction.close()\n\
\n\
    plotter.show()\n\
\n\
    smgr.steer()\n\
\n\
  del plotter\n\
\n\
del smgr\n\
del r\n\
del h\n\
";

  ::PyRun_SimpleString((char*)s.c_str());

  if(::Py_IsInitialized()) ::Py_Finalize();

#ifdef INLIB_MEM
  }inlib::mem::balance(std::cout);
#endif

  return 0;
}
