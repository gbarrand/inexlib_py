/**

@page inexlib_py_introduction <h1>Introduction</h1>

  inexlib_py is the collection of exlib examples related to Python put in a standalone package.
 The 1.1.x contains examples coworking with Spark. It can be built with Python3. The 1.2.x
 contains examples that have a "client" mode so that they can send scene graphs to the
 inexlib_serv application.

@section inexlib_py_examples Examples
  There are C++ little applications that activate Python through it's library and
 a set of .py scripts that demonstrate how to activate inlib/exlib from a Python prompt by using
 the SWIG modules:
@verbatim
     inlib_swig_py.so            # pure inlib.
     exlib_window_swig_py.so     # on screen inlib/exlib graphics and plotting.
     exlib_offscreen_swig_py.so  # offscreen inlib/exlib graphics and plotting.
@endverbatim
 These modules has been done by using the SWIG wrapping of some (but not all) classes of inlib and exlib.

  C++ apps (source code in inexlib_py/inexlib/exlib/examples/cpp):
@verbatim
    hello_py.cpp            # to check Python activation from C++.
    h1d_spy.cpp             # inlib histogram wrapped with swig.
    plotter_spy_screen.cpp  # exlib plotting wrapped with swig.
    mandel_py.cpp           # check calling a C++ function from Python.
@endverbatim
  C++ inlib "client" apps (source code in inexlib_py/inexlib/inlib/examples/cpp):
@verbatim
    cube_to_sg_serv.cpp     # send a cube to inexlib_serv.
    lego_to_sg_serv.cpp     # send a lego plot to inexlib_serv.
@endverbatim
 Python .py scripts:
@verbatim
    h1d.py                 # inlib histo.
    rroot.py               # read an histo in a root file.
    waxml.py               # write histos at the AIDA XML file format.
    tree.py                # project a ntuple found in the pawdemo.root file
                           # and plot the histo.
    
    polyhedron_vis.py      # visualise a solid/shape boolean operation.
    plotter_window.py      # plot an histo by using softinex graphics and plotting.
                           # A simple viewer is used.
    plotter_vis.py         # same as upper but by using a more advanced "gui viewer".
    cfitsio_hst_vis.py     # visualise an image in a fits file.
    rdirs_vis.py           # random clouds of points in a plot.
    two_cubes_vis.pye      # show the "blender effect" on a coarse grained rearranged
                           # random points.
    
    c3d_vis.py             # create, fill and plot a 3D cloud of 3D random points.
    csv_c3d_vis.py         # read points from cosmo_dc2_rdz_cut.csv, fill and plot a 3D cloud.
    csv_h1d_vis.py         # read points from cosmo_dc2_rdz_cut.csv, fill and plot histos.
    csv_vertices_vis.py    # read points from cosmo_dc2_rdz_cut.csv, and visualize them
                           # with a simple viewer (without a plot).
    csv_vertices_gui_viewer_vis.py # same as upper, but by using a more advanced viewer.
@endverbatim

 Spark examples:
@verbatim
    spark_inlib_h1d_vis.py   # inlib histo.
    spark_fits.py            # open spark_test_data.fits and a simple collect.
    spark_fits_ntuple_vis.py # read a TBL in a fits file, do "ntuple projections" with Spark,
                             # and plot with the inexlib/plotter.
    spark_fits_vis.py        # open spark_test_data.fits, do a simple collect, fill and
                             # plot an histo.

 The scripts:						
    spark_parquet_vis.py
    spark_parquet_radec_vis.py
    spark_parquet_colored_galaxies_vis.py
 uses parquet files not in the distribution.
@endverbatim

  See the README file on github for instructions on how to build, install and run.

@section inexlib_py_swig What is wrapped ?

  What is available of inlib/exlib from Python can be seen in the ".i" files given to SWIG.
 These are available on github at :
@verbatim
    inexlib_py/inexlib/exlib/exlib/swig
@endverbatim
 
 In particular the file nodes.i shows the inlib::sg::nodes declared to SWIG along their "fields" ("sf" for a simple field
 or "mf" for a multiple field). For example for inlib::sg::cube, what is declared to SWIG is :
@verbatim
    class cube : public node {
    public:
      virtual node* copy() const;
    public:
      cube();
      virtual ~cube();
      cube(const cube&);
      cube& operator=(const cube&);
    public:  
      sf<float> width;    //simple field for the width of the cube.
      sf<float> height;
      sf<float> depth;
    };
@endverbatim
 The upper permits, from Python, to do something as :
@verbatim
    import inlib
    cube = inlib.sg_cube()
    cube.width.value(3)
@endverbatim

  Note that we do not wrap all the C++ code with SWIG. In general in a C++ class, there are private  and protected
 materials that are for developers and do not need to be seen from Python. The remaining public material can be split
 in "public/developer" and "public/user". "public/developer" material is for the developer to help classes working together.
 And the remaining "public/user" fields and methods are the "true" materials that a user want to see; it is the "spirit" for
 what the class and package had been created. In inexlib_py, we declare to SWIG only the C++ which is "public/user".
 For the moment, we do not have a nice web reference manual "a la doxygen" for the ".i", then the best is to jump directly
 in the .i files to have informations. What is here is in general self explanatory and should be already helpfull.

*/

