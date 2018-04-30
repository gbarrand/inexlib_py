// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

//exlib_build_use Python inlib thread exlib
//exlib_build_cppfile ../../exlib/spy/inlib_swig_py.cpp

#include <exlib/Python>

extern "C" {
  void initinlib_swig_py();
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
  inlib::putenv(s_PYTHONPATH(),"../../exlib/spy"); //to find inlib.py

  if(!::Py_IsInitialized()) ::Py_Initialize();
  ::PyEval_InitThreads();

  ::PyRun_SimpleString((char*)"print 'hello h1d_py'");

  initinlib_swig_py();

  std::string s = "\n\
import inlib\n\
h = inlib.histo_h1d('Rand gauss',100,-5,5)\n\
\n\
r = inlib.rgaussd(0,1)\n\
for I in range(0,10000):\n\
  h.fill(r.shoot(),1)\n\
\n\
print h.entries(),h.mean(),h.rms()\n\
import math\n\
print 'exp(1) = ',math.exp(1)\n\
";

  ::PyRun_SimpleString((char*)s.c_str());

  if(::Py_IsInitialized()) ::Py_Finalize();

#ifdef INLIB_MEM
  }inlib::mem::balance(std::cout);
#endif

  return 0;
}
