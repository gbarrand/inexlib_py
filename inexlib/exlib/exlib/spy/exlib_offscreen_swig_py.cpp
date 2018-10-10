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
#include "../fits_image"

#include <inlib/sg/infos>

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

#include "exlib_offscreen_swig_py.icc"

//exlib_build_use inlib freetype gl2ps GL
//exlib_build_use csz kernel cfitsio

//exlib_build_use Python


