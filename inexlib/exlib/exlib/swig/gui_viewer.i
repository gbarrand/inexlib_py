// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

namespace exlib {
namespace EXLIB_SWIG_XANY {

class gui_viewer : public inlib::sg::gui_viewer {
public:
  gui_viewer(session& a_session,
             int a_x = 0,int a_y = 0,
             unsigned int a_width = 500,unsigned int a_height = 500);
  virtual ~gui_viewer();
protected:
  gui_viewer(const gui_viewer& a_from);
  gui_viewer& operator=(const gui_viewer& a_from);
public:
  bool has_window() const;
  bool show();
  bool steer();
};

}}

//exlib_build_use skip
