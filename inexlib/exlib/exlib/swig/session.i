// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

// generic X11/Windows wrapper.

namespace exlib {
namespace EXLIB_SWIG_XANY {

class session {
public:
  session(std::ostream& a_out);
  virtual ~session();
public:
  session(const session& a_from);
  session& operator=(const session&);
public:
  std::ostream& out();
  bool is_valid();
  bool steer();
  bool sync();
};

}}

//exlib_build_use skip
