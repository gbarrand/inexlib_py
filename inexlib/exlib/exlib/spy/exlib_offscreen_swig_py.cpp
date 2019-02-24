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
#include "../sg/text_freetype"
#include "../sg/write_paper"
#include "../fits_image"
#include "../xml/xml_style"
#include "../zlib"

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

#include "exlib_offscreen_swig_py.icc"

//exlib_build_use inlib freetype gl2ps GL
//exlib_build_use csz kernel cfitsio socket
//exlib_build_use zlib expat

//exlib_build_use png jpeg

//exlib_build_use Python


