/**
@page inexlib_py_download Download

  Source and some binaries are on github :
<p>
  <a href="https://github.com/gbarrand/inexlib_py.git" target="_blank">https://github.com/gbarrand/inexlib_py.git</a>
</p>

  WARNING, ATTENTION, ACHTUNG: our computers are now like Florida, there are Pythons everywhere.
 For example, on macOS, you may have a Python under /System and, if using Macports, another one somewhere
 under /opt/local and, if using various anaconda installations, other ones within them.
 When building/running inexlib_py you must be aware than multiple Python installations may be present
 on your machine and you must be cautious, at run time, to use the Python program corresponding to the
 Python toolkit used to compile and link the inlib_swig_py.so, exlib_offscreen_swig_py.so,
 exlib_window_swig_py.so and the compiled example applications.

  When building, the access to Python to build is in the shell script:
@verbatim
    <install_path>/bush/use/Python
@endverbatim
 The upper is for using a Python2.x, which is the default in bush scripts.
 If using a Python3, it is in:     
@verbatim
    <install_path>/bush/use/Python3
@endverbatim
 Then, if needed, customize these files according your chosen Python installation.

  When running, you may have to customize accordingly the "run, spark_run" scripts of the distribution
 packing. You may have to customize these scripts under "Python setup" to be sure to activate the Python
 used to build the inexlib_py kit. You may have to look to have a correct "py_exe" variable and perhaps
 the correct LD_LIBRARY_PATH (DYLD_LIBRARY_PATH on macOS) environment variable to attach the correct
 shared libs. run (and spark_run) sets the PYTHONPATH, but it should be ok without customization.

*/
