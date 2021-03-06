// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

//exlib_build_use Python inlib thread exlib


inline double mandel(double XP,double YP) {
  int NMAX = 30;
  int N;
  double X=XP;
  double Y=YP;
  double XX=0.;
  double YY=0.;
  for(N=1;N<=NMAX;N++) {
    double TT=XX*XX-YY*YY+X;
    YY=2.*XX*YY+Y;
    XX=TT;
    if(4.<(XX*XX+YY*YY)) break;
  }
  return ((double)N)/((double)NMAX);
}

#include <exlib/Python>
#include <inlib/system>
#include <inlib/file>
#include <inlib/sys/dir>

#include <inlib/S_STRING>
INLIB_GLOBAL_STRING(PYTHONHOME)
INLIB_GLOBAL_STRING(PYTHONPATH)

#include <iostream>
#include <cstdlib>

int main() {
  
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
  //so that python find mandel.py :
  if(inlib::file::exists("../../data/mandel.py")) { //if run from exlib/examples/cpp.
    inlib::putenv(s_PYTHONPATH(),"../../data");
  } else if(inlib::file::exists("./data/mandel.py")) { //if run from inexlib_py distribution.
    inlib::putenv(s_PYTHONPATH(),"./data");
  } else if(inlib::file::exists("mandel.py")) {
    inlib::putenv(s_PYTHONPATH(),".");
  } else {
    if(!inlib::is_env(s_PYTHONPATH())) {
      std::cout << "environment variable PYTHONPATH not defined and we can't define it since we don't know where mandel.py is."
		<< std::endl;
      return EXIT_FAILURE;
    }      
  }

  if(!::Py_IsInitialized()) ::Py_Initialize();
  if(!::Py_IsInitialized()) {
    std::cout << "can't initialize Python." << std::endl;
    return EXIT_FAILURE;
  }
    
#if PY_VERSION_HEX >= 0x03000000
  PyObject* pName = ::PyUnicode_FromString("mandel");
#else  
  PyObject* pName = ::PyString_FromString("mandel");
#endif  
  if(!pName) {
    ::PyErr_Print();
    std::cout << "PyString_FromString() failed." << std::endl;
    return EXIT_FAILURE;
  }
  
  PyObject* pModule = ::PyImport_Import(pName);
  if(!pModule) {
    ::PyErr_Print();
    std::cout << "PyImport_Import() failed." << std::endl;
    return EXIT_FAILURE;
  }
  
  PyObject* pDict = ::PyModule_GetDict(pModule);
  if(!pDict) {
    ::PyErr_Print();
    std::cout << "PyModule_GetDict() failed." << std::endl;
    return EXIT_FAILURE;
  }
  
  PyObject* pFunc = ::PyDict_GetItemString(pDict,"mandel");
  if(!pFunc) {
    ::PyErr_Print();
    std::cout << "PyDict_GetItemString() failed." << std::endl;
    return EXIT_FAILURE;
  }
  
  if(!::PyCallable_Check(pFunc)) {
    ::PyErr_Print();
    std::cout << "PyCallable_Check() failed." << std::endl;
    return EXIT_FAILURE;
  }

  double XP = 0.5;
  double YP = 1.6;
  
  PyObject* pValue = Py_BuildValue("dd",XP,YP);
  if(!pValue) {
    ::PyErr_Print();
    std::cout << "Py_BuildValue() failed." << std::endl;
    return EXIT_FAILURE;
  }
    
  PyObject* presult = PyObject_CallObject(pFunc,pValue);
  if(!presult) {
    ::PyErr_Print();
    std::cout << "PyObject_CallObject() failed." << std::endl;
    return EXIT_FAILURE;
  }

  double p_res = PyFloat_AsDouble(presult);
  //std::cout << "Result is " << PyFloat_AsDouble(presult) << std::endl;

  double c_res = mandel(XP,YP);
  if(p_res!=c_res) {
    std::cout << "bad Python result " << p_res << ", expected " << c_res << std::endl;
  }
  
  //Py_DECREF(pDict);
  //Py_DECREF(pFunc);
  Py_DECREF(presult);  
  Py_DECREF(pValue);
  Py_DECREF(pModule);
  Py_DECREF(pName);

  ::Py_Finalize();

  return EXIT_SUCCESS;
}
