// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

// used to test the creation of a new swig module.

%module test

namespace inlib {

class my_class {
public:
  my_class();
  virtual ~my_class();
public:  
  my_class(const my_class&);
  my_class& operator=(const my_class&);
public:
  static void s_method();
  void method();
public:
  static int s_int;
public:  
  int m_int;
};

class my_class_2 {
public:
  my_class_2();
  virtual ~my_class_2();
public:  
  my_class_2(const my_class_2&);
  my_class_2& operator=(const my_class_2&);
public:
  static void s_method();
  void method();
public:
  static int s_int;
public:  
  int m_int;
};

}
 
//exlib_build_use skip
