// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

namespace exlib {
namespace EXLIB_SWIG_XANY {

class sg_viewer {
public:
  sg_viewer(session& a_session,
            int a_x = 0,int a_y = 0,
            unsigned int a_width = 500,unsigned int a_height = 500);
  virtual ~sg_viewer();
protected:
  sg_viewer(const sg_viewer&);
  sg_viewer& operator=(const sg_viewer&);
public:
  bool has_window() const;
  bool show();
  unsigned int width() const;
  unsigned int height() const;
  inlib::sg::group& sg();
  const inlib::sg::group& sg() const;
};

}}

//exlib_build_use skip
