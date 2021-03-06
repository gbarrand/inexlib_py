// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

#include "../swig/inlib_i"

#ifdef EXLIB_USE_NATIVE_FREETYPE
#include <ft2build.h>
#else
#include <ourex_ft2build.h>
#endif
#include FT_FREETYPE_H
#include FT_GLYPH_H
#include FT_OUTLINE_H

#include "../sg/gl2ps_action"
#include "../sg/write_paper"
#include "../fits_image"
#include "../xml/xml_style"
#include "../zlib"

#if defined(__APPLE__)
#include <TargetConditionals.h>
#if TARGET_OS_IPHONE
#else
#include "../Cocoa/plotter.hm"
#include "../Cocoa/sg_viewer.hm"
#include "../Cocoa/gui_plotter.hm"
#define EXLIB_SWIG_XANY Cocoa
#endif
#else //not __APPLE__
#ifdef _WIN32
#include "../Windows/plotter"
#include "../Windows/sg_viewer"
#include "../Windows/gui_plotter"
#define EXLIB_SWIG_XANY Windows
#else //not _WIN32
#include "../X11/plotter"
#include "../X11/sg_viewer"
#include "../X11/gui_plotter"
#define EXLIB_SWIG_XANY X11
#endif //_WIN32
#endif //__APPLE__

#if defined(__linux)
// Clash between os_defines.h (coming from <string>) and pyconfig.h
#if defined(_POSIX_C_SOURCE)
#undef _POSIX_C_SOURCE
#endif
#if defined(_XOPEN_SOURCE)
#undef _XOPEN_SOURCE
#endif
#endif

// to remove warnings coming from jpeg/jconfig.h (from exlib/<screen>/gui_plotter) and existing also in Python.h :
#ifdef HAVE_PROTOTYPES
#undef HAVE_PROTOTYPES
#endif
#ifdef HAVE_STDLIB_H
#undef HAVE_STDLIB_H
#endif

#include <Python.h>

#ifdef _WIN32
#include <windows.h>
#undef max
#undef ERROR
#undef DELETE
#endif

#include "exlib_window_swig_py.icc"

//exlib_build_use inlib freetype gl2ps GL
//exlib_build_use csz kernel cfitsio socket
//exlib_build_use png jpeg zlib expat

//exlib_build_use screen

//exlib_build_use Python



