// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

namespace exlib {
namespace EXLIB_SWIG_XANY {

class plotter {
public:
  plotter(session& a_session,
          unsigned int a_cols = 1,unsigned int a_rows = 1,
          int a_x = 0,int a_y = 0,
          unsigned int a_width = 500,unsigned int a_height = 500);
  virtual ~plotter();
protected:
  plotter(const plotter& a_from);
  plotter& operator=(const plotter& a_from);
public:
  bool has_window() const;
  bool show();
  bool steer();
  unsigned int width() const;
  unsigned int height() const;
  inlib::sg::group& sg();
  const inlib::sg::group& sg() const;
public:
  inlib::sg::plots& plots();
  const inlib::sg::plots& plots() const;
  inlib::sg::plottable* plot(const inlib::histo::h1d& a_histo);
  inlib::sg::plottable* plot(const inlib::histo::h2d& a_histo);
  inlib::sg::plottable* plot(const inlib::histo::p1d& a_histo);
  inlib::sg::plottable* plot(const inlib::histo::c2d& a_cloud);
  inlib::sg::plottable* plot(const inlib::histo::c3d& a_cloud);
  inlib::sg::plottable* plot_cp(const inlib::histo::h1d& a_histo);
  inlib::sg::plottable* plot_cp(const inlib::histo::h2d& a_histo);
  inlib::sg::plottable* plot_cp(const inlib::histo::p1d& a_histo);
  inlib::sg::plottable* plot_cp(const inlib::histo::c2d& a_cloud);
  inlib::sg::plottable* plot_cp(const inlib::histo::c3d& a_cloud);
};

}}

//exlib_build_use skip
