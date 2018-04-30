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
#include <inlib/S_STRING>
INLIB_GLOBAL_STRING(PYTHONHOME)
INLIB_GLOBAL_STRING(PYTHONPATH)

#include <iostream>
#include <cstdlib>

int main() {
  
#ifdef ourex_Python_h
  if(!inlib::is_env(s_PYTHONHOME())) {
    inlib::putenv(s_PYTHONHOME(),"../../../ourex/Python");
  }
#endif
  inlib::putenv(s_PYTHONPATH(),"../../data");

  if(!::Py_IsInitialized()) ::Py_Initialize();
  if(!::Py_IsInitialized()) {
    std::cout << "can't initialize Python." << std::endl;
    return EXIT_FAILURE;
  }
    
  PyObject* pName = ::PyString_FromString("mandel");
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
