// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

%rename(session) exlib::EXLIB_SWIG_XANY::session;
#include "session.i"

%rename(plotter) exlib::EXLIB_SWIG_XANY::plotter;
#include "plotter.i"

%rename(gui_viewer_window) exlib::EXLIB_SWIG_XANY::gui_viewer;
#include "gui_viewer.i"

%rename(gui_plotter) exlib::EXLIB_SWIG_XANY::gui_plotter;
#include "gui_plotter.i"

%rename(sg_viewer) exlib::EXLIB_SWIG_XANY::sg_viewer;
#include "viewer.i"

//exlib_build_use skip
