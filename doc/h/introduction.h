/**

@page inexlib_py_introduction Introduction

  inexlib_py is the collection of exlib examples related to Python put in a standalone package
 and distribution. The 1.1.x contains also examples coworking with Spark. It can be built
 with Python3.

  There are little applications, written in C++, that activates Python through its library and
 a set of .py scripts that demonstrate how to activate inlib/exlib from a Python prompt by using
 the modules 
@verbatim
     inlib_swig_py.so            # pure inlib.
     exlib_window_swig_py.so     # on screen inlib/exlib graphics and plotting.
     exlib_offscreen_swig_py.so  # offscreen inlib/exlib graphics and plotting.
@endverbatim
 Thes modules has been done by using the SWIG wrapping of some (but not all) classes of inlib and exlib.

  C++ apps (source code in inexlib_py/inexlib/exlib/examples/cpp) :
@verbatim
    hello_py.cpp            # to check Python activation from C++.
    h1d_spy.cpp             # inlib histogram wrapped with swig.
    plotter_spy_screen.cpp  # exlib plotting wrapped with swig.
    mandel_py.cpp           # check calling a C++ function from Python.
@endverbatim
 and .py scripts :
@verbatim
    h1d.py          # inlib histo.
    rroot.py        # read an histo in a root file.
    plotter.py      # plot an histo by using softinex graphics and plotting.
    tree.py         # project a ntuple found in the pawdemo.root file and plot the histo.
    waxml.py        # write histos at the AIDA XML file format.
    polyhedron.py   # visualise a solid/shape boolean operation.
    cfitsio_hst.py  # visualise an image in a fits file.
@endverbatim

 For Spark examples :
@verbatim
    spark_hello.py            # hello from the C++ inlib::spark_greet().
    spark_h1d.py              # inlib histo.
    spark_c3d_window.py       # do a spark action, get (x,y,z) lists,
                              # and plot the 3D cloud with a inlib-exlib/plotter.
    spark_c3d_gui_window.py   # the same, but by using a "gui viewer" similar
                              # to the ioda viewer. See softinex/"Apps general behaviour"
                              # for explanations about the button panels.
    spark_c3d_offscreen.py    # do a spark action, get (x,y,z) lists,
                              # and plot the 3D cloud "offscreen" by producing an out.ps
                              # Postscript file (done with gl2ps).
    spark_cfitsio_ntuple.py   # read a TBL in a fits file, do "ntuple projections" with Spark,
                              # and plot with the inexlib/plotter.
@endverbatim

  See the README on github for instructions on how to build, install and run.

*/

