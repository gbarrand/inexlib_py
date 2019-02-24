// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

//exlib_build_use inlib Python thread

#include <Python.h> //must come before other includes.

#include <string>

int main(int,char**) {

  if(!::Py_IsInitialized()) ::Py_Initialize();
  ::PyEval_InitThreads();

  std::string s("print('hello python from C')\nprint('end')");
  ::PyRun_SimpleString((char*)s.c_str());

  if(::Py_IsInitialized()) ::Py_Finalize();

  return 0;
}
