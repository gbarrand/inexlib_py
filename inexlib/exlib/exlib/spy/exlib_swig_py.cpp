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
#include "../fits_image"

#include <inlib/sg/infos>

#ifdef _WIN32
#include "../Windows/plotter"
#include "../Windows/sg_viewer"
#define EXLIB_SWIG_XANY Windows
#else
#include "../X11/plotter"
#include "../X11/sg_viewer"
#define EXLIB_SWIG_XANY X11
#endif

#if defined(__linux)
// Clash between os_defines.h (coming from <string>) and pyconfig.h
#if defined(_POSIX_C_SOURCE)
#undef _POSIX_C_SOURCE
#endif
#if defined(_XOPEN_SOURCE)
#undef _XOPEN_SOURCE
#endif
#endif

#include <Python.h>

#ifdef _WIN32
#include <windows.h>
#undef max
#undef ERROR
#undef DELETE
#endif

#include "exlib_swig_py.icc"

//exlib_build_use inlib Python freetype gl2ps GL
//exlib_build_use csz
//exlib_build_use screen kernel
//exlib_build_use cfitsio


