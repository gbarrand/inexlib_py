// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

//exlib_build_use inlib thread exlib
//exlib_build_use Python

#include <exlib/Python>

extern "C" {
#if PY_VERSION_HEX >= 0x03000000
  PyObject* PyInit_inlib_swig_py();
#else  
  void initinlib_swig_py();
#endif  
}

#include <inlib/mem>
#include <inlib/system>
#include <inlib/file>
#include <inlib/sys/dir>
#include <inlib/app>

#include <inlib/S_STRING>
INLIB_GLOBAL_STRING(PYTHONHOME)
INLIB_GLOBAL_STRING(PYTHONPATH)

#include <string>
#include <iostream>

int main(int,char** argv) {
#ifdef INLIB_MEM
  inlib::mem::set_check_by_class(true);{
#endif

  std::string exe_path; //for res_dir
  if(!inlib::program_path(argv[0],exe_path)) {
    std::cout << "can't get exe directory." << std::endl;
    return EXIT_FAILURE;
  }

#ifdef ourex_Python_h
  if(!inlib::is_env(s_PYTHONHOME())) {
    std::string path = "../../../ourex/Python";
    if(!inlib::dir::is_a(path)) {
      std::cout << "can't find directory "<< inlib::sout(path) << " ." << std::endl;
      return EXIT_FAILURE;
    }
    inlib::putenv(s_PYTHONHOME(),path);
  }
#endif

  //so that python find inlib.py :
 {std::string res_dir;
  inlib::app_res_dir(exe_path,res_dir);
#if PY_VERSION_HEX >= 0x03000000
  std::string spy("spy3");
#else
  std::string spy("spy");
#endif
  std::string path = res_dir+"/"+spy;
  if(!inlib::dir::is_a(path)) {
    std::cout << "can't find directory "<< inlib::sout(path) << " ." << std::endl;
    return EXIT_FAILURE;
  }
  inlib::putenv(s_PYTHONPATH(),path);}

#if PY_VERSION_HEX >= 0x03000000
  ::PyImport_AppendInittab("inlib_swig_py", &PyInit_inlib_swig_py);
#endif
  
  if(!::Py_IsInitialized()) ::Py_Initialize();
  ::PyEval_InitThreads();

  ::PyRun_SimpleString((char*)"print('hello h1d_py')");

#if PY_VERSION_HEX >= 0x03000000
#else  
  initinlib_swig_py();
#endif  

  std::string s = "\n\
import inlib\n\
h = inlib.histo_h1d('Rand gauss',100,-5,5)\n\
\n\
r = inlib.rgaussd(0,1)\n\
for I in range(0,10000):\n\
  h.fill(r.shoot(),1)\n\
\n\
print(h.entries())\n\
print(h.mean())\n\
print(h.rms())\n\
import math\n\
print('exp(1) :')\n\
print(math.exp(1))\n\
";

  ::PyRun_SimpleString((char*)s.c_str());

  if(::Py_IsInitialized()) ::Py_Finalize();

#ifdef INLIB_MEM
  }inlib::mem::balance(std::cout);
#endif

  return 0;
}
