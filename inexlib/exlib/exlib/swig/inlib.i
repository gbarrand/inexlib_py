// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
%include std_string.i

%include std_vector.i
//%template(std_vector_string)  std::vector<std::string>;
%template(std_vector_uint)    std::vector<unsigned int>;
%template(std_vector_int)     std::vector<int>;
%template(std_vector_float )  std::vector<float>;
%template(std_vector_double)  std::vector<double>;

%include <inlib/get_cout>

//#ifdef SWIGLUA
//#else
//%include std_iostream.i
//#endif

//%include std_pair.i
//%include std_map.i

//////////////////////////////////////////////////////////////////////////////
/// system ///////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
namespace inlib {
bool env_append_path(const std::string&,const std::string&);

const std::string& sep();

// used to SWIG wrap functions/methods that uses std::string& in arguments (then a writeable argument) :
class std_string {
public:
  std_string();
  std_string(const std::string&);
  virtual ~std_string();
  std_string(const std_string&);
  std_string& operator=(const std_string&);
public:
  const std::string& cast() const {return *this;}
};

class printer {
public:
  printer(std::ostream&);
  virtual ~printer();
  printer(const printer&);
  printer& operator=(const printer&);
public:
  void write(const std::string&);
};

class args {
public:
  args();
  virtual ~args();
  args(const args&);
  args& operator=(const args&);
public:  
  bool add(const std::string&,const std::string& a_value = "",bool a_override = true);
  int remove(const std::string&);
  void remove_first();
};

//namespace file {
//const std::string& s_format_guessed();
//const std::string& s_format_iv();
//}

namespace sg {
class guiv {
private:
  guiv(std::ostream&,unsigned int,unsigned int,bool);
  virtual ~guiv();
  guiv(const guiv&);
  guiv& operator=(const guiv&);
};
}
 
class opener {
public:
  opener(sg::guiv&,unsigned int);
  virtual ~opener();
  opener(const opener&);
  opener& operator=(const opener&);
//public:
//virtual bool open(const std::string&,const std::string&,const args&,bool&);
};
%extend opener {
  bool open(const std::string& a_path) {
    bool done;
    return self->open(a_path,inlib::file::s_format_guessed(),inlib::args(),done);
  }
}

}

%rename(file_exists)                 inlib::file::exists;
%rename(file_write)                  inlib::file::write;
%rename(file_paper_format_extension) inlib::file::paper_format_extension;

namespace inlib {
namespace file {

bool exists(const std::string&);
bool write(const std::string&,const std::string&);
bool write(const std::string&,const std::vector<std::string>&);

bool paper_format_extension(const std::string& a_format,std_string&);

}}

//////////////////////////////////////////////////////////////////////////////
/// histo ////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
%rename(histo_h1d)    inlib::histo::h1d;
%rename(histo_h2d)    inlib::histo::h2d;
%rename(histo_p1d)    inlib::histo::p1d;
%rename(histo_p2d)    inlib::histo::p2d;
%rename(histo_c2d)    inlib::histo::c2d;
%rename(histo_c3d)    inlib::histo::c3d;

namespace inlib {
namespace histo {

class h1d {
public:
  h1d(const std::string&,unsigned int,double,double);
  virtual ~h1d();
public:
  h1d(const h1d&);
  h1d& operator=(const h1d&);
public:
  bool fill(double,double);
  unsigned int entries() const;
  double mean() const;
  double rms() const;
};

class h2d {
public:
  h2d(const std::string&,unsigned int,double,double,unsigned int,double,double);
  virtual ~h2d();
public:
  h2d(const h2d&);
  h2d& operator=(const h2d&);
public:
  bool fill(double,double,double);
  unsigned int entries() const;
  double mean_x() const;
  double rms_x() const;
  double mean_y() const;
  double rms_y() const;
};


class p1d {
public:
  p1d(const std::string&,unsigned int,double,double);
  p1d(const std::string&,unsigned int,double,double,double,double);
  virtual ~p1d();
public:
  p1d(const p1d&);
  p1d& operator=(const p1d&);
public:
  bool fill(double,double,double);
  unsigned int entries() const;
  double mean() const;
  double rms() const;
};

class p2d {
public:
  p2d(const std::string&,unsigned int,double,double,unsigned int,double,double);
  p2d(const std::string&,unsigned int,double,double,unsigned int,double,double,double,double);
  virtual ~p2d();
public:
  p2d(const p2d&);
  p2d& operator=(const p2d&);
public:
  bool fill(double,double,double,double);
  unsigned int entries() const;
  double mean_x() const;
  double rms_x() const;
  double mean_y() const;
  double rms_y() const;
};

class c2d {
public:
  c2d(const std::string&);
  virtual ~c2d();
public:
  c2d(const c2d&);
  c2d& operator=(const c2d&);
public:
  bool fill(double,double,double);
  unsigned int entries() const;
  double lower_edge_x() const;
  double upper_edge_x() const;
  double lower_edge_y() const;
  double upper_edge_y() const;
  double mean_x() const;
  double rms_x() const;
  double mean_y() const;
  double rms_y() const;
};

class c3d {
public:
  c3d(const std::string&);
  virtual ~c3d();
public:
  c3d(const c3d&);
  c3d& operator=(const c3d&);
public:
  bool fill(double,double,double,double);
  unsigned int entries() const;
  double lower_edge_x() const;
  double upper_edge_x() const;
  double lower_edge_y() const;
  double upper_edge_y() const;
  double lower_edge_z() const;
  double upper_edge_z() const;
  double mean_x() const;
  double rms_x() const;
  double mean_y() const;
  double rms_y() const;
  double mean_z() const;
  double rms_z() const;
};

}}

//////////////////////////////////////////////////////////////////////////////
/// random ///////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

namespace inlib {

class rtausmeui {
public:
  rtausmeui(unsigned int a_seed = 1);
  virtual ~rtausmeui();
public:
  rtausmeui(const rtausmeui&);
  rtausmeui& operator=(const rtausmeui&);
public:
  void set_seed(unsigned int a_seed);
  unsigned int seed() const;
  unsigned int shoot();
};

class rtausmed {
public:
  rtausmed(unsigned int a_seed = 4357);
  virtual ~rtausmed();
public:
  rtausmed(const rtausmed&);
  rtausmed& operator=(const rtausmed&);
public:
  void set_seed(unsigned int);
  unsigned int seed() const;
  double shoot();
};

class rgaussd {
public:
  rgaussd(double,double);
  virtual ~rgaussd();
public:
  rgaussd(const rgaussd&);
  rgaussd& operator=(const rgaussd&);
public:
  double shoot();
};

class rbwd {
public:
  rbwd(double,double);
  virtual ~rbwd();
public:
  rbwd(const rbwd&);
  rbwd& operator=(const rbwd&);
public:
  double shoot();
};

class rexpd {
public:
  rexpd(double);
  virtual ~rexpd();
public:
  rexpd(const rexpd&);
  rexpd& operator=(const rexpd&);
public:
  double shoot();
};

class rdir2d {
public:
  rdir2d();
  virtual ~rdir2d();
public:
  rdir2d(const rdir2d&);
  rdir2d& operator=(const rdir2d&);
};
%extend rdir2d {
  //std::vector<double> shoot() const {
  //  std::vector<double> v(2);
  //  self->shoot(v[0],v[1]);
  //  return v;
  //}
  void shoot(std::vector<double>& a_v) const {
    if(a_v.size()<2) a_v.resize(2);
    self->shoot(a_v[0],a_v[1]);
  }
}

class rdir3d {
public:
  rdir3d();
  virtual ~rdir3d();
public:
  rdir3d(const rdir3d&);
  rdir3d& operator=(const rdir3d&);
};  
%extend rdir3d {
  //std::vector<double> shoot() const {
  //  std::vector<double> v(3);
  //  self->shoot(v[0],v[1],v[2]);
  //  return v;
  //}
  void shoot(std::vector<double>& a_v) const {
    if(a_v.size()<3) a_v.resize(3);
    self->shoot(a_v[0],a_v[1],a_v[2]);
  }
}

}

//////////////////////////////////////////////////////////////////////////////
/// xml //////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

%rename(sg_style_colormap)          inlib::sg::style_colormap;
%rename(sg_style_default_colormap)  inlib::sg::style_default_colormap;
%rename(sg_style_ROOT_colormap)     inlib::sg::style_ROOT_colormap;
%rename(xml_styles)                 inlib::xml::styles;

namespace inlib {
namespace sg {

class style_colormap {
public:
  style_colormap();
  virtual ~style_colormap();
public:
  style_colormap(const style_colormap&);
  style_colormap& operator=(const style_colormap&);
};

class style_default_colormap : public style_colormap {
public:
  style_default_colormap();
  virtual ~style_default_colormap();
public:
  style_default_colormap(const style_default_colormap&);
  style_default_colormap& operator=(const style_default_colormap&);
};

class style_ROOT_colormap : public style_colormap {
public:
  style_ROOT_colormap();
  virtual ~style_ROOT_colormap();
public:
  style_ROOT_colormap(const style_ROOT_colormap&);
  style_ROOT_colormap& operator=(const style_ROOT_colormap&);
};

}}

namespace inlib {
namespace xml {

class styles {
public:
  styles(std::ostream&);
  virtual ~styles();
public:
  styles(const styles&);
  styles& operator=(const styles&);
public:  
  std::ostream& out() const;
  void add_colormap(const std::string& a_name,const sg::style_colormap&);
};

}}

#include "picmap.i"

namespace inlib {

template <class T>
class img {
public:
  img();
  virtual ~img();
public:
  img(const img&);
  img& operator=(const img&);
public:  
  void transfer(img&);
  void clear();
  bool copy(const img&);
  void make_empty(bool a_delete = true);
  bool is_empty() const;
  bool equal(const img&) const;
  unsigned int width() const;
  unsigned int height() const;
  unsigned int bytes_per_pixel();
  unsigned int bpp() const;
  bool owner() const;
  unsigned int size() const; //bytes
};
 
template <class TB>
class lut {
public:  
  lut(const TB&,const TB&,size_t);
  virtual ~lut();
public:
  lut(const lut&);
  lut& operator=(const lut&);
public:
  size_t apply(const TB&) const;
public:
  TB mn() const;
  TB mx() const;
  size_t coln() const;
};

}

%template(img_byte)      inlib::img<inlib::byte>;
%template(lut_float)     inlib::lut<float>;
%template(lut_double)    inlib::lut<double>;

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
#include "math.i"
//////////////////////////////////////////////////////////////////////////////
/// sg ///////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

namespace inlib {

class colorf {
public:
  colorf();
  colorf(float,float,float,float = 1);
  virtual ~colorf();
  colorf(const colorf&);
  colorf& operator=(const colorf&);
public:  
  float r() const;
  float g() const;
  float b() const;
  float a() const;
  void set_r(float);
  void set_g(float);
  void set_b(float);
  void set_a(float);
};
 
const colorf& colorf_aquamarine();
const colorf& colorf_mediumaquamarine();
const colorf& colorf_black();
const colorf& colorf_blue();
const colorf& colorf_cadetblue();
const colorf& colorf_cornflowerblue();
const colorf& colorf_darkslateblue();
const colorf& colorf_lightblue();
const colorf& colorf_lightsteelblue();
const colorf& colorf_mediumblue();
const colorf& colorf_mediumslateblue();
const colorf& colorf_midnightblue();
const colorf& colorf_navyblue();
const colorf& colorf_navy();
const colorf& colorf_skyblue();
const colorf& colorf_slateblue();
const colorf& colorf_steelblue();
const colorf& colorf_coral();
const colorf& colorf_cyan();
const colorf& colorf_firebrick();
const colorf& colorf_brown();
const colorf& colorf_gold();
const colorf& colorf_goldenrod();
const colorf& colorf_green();
const colorf& colorf_darkgreen();
const colorf& colorf_darkolivegreen();
const colorf& colorf_forestgreen();
const colorf& colorf_limegreen();
const colorf& colorf_mediumseagreen();
const colorf& colorf_mediumspringgreen();
const colorf& colorf_palegreen();
const colorf& colorf_seagreen();
const colorf& colorf_springgreen();
const colorf& colorf_yellowgreen();
const colorf& colorf_darkslategrey();
const colorf& colorf_dimgrey();
const colorf& colorf_lightgrey();
const colorf& colorf_grey();
const colorf& colorf_khaki();
const colorf& colorf_magenta();
const colorf& colorf_maroon();
const colorf& colorf_orange();
const colorf& colorf_orchid();
const colorf& colorf_darkorchid();
const colorf& colorf_mediumorchid();
const colorf& colorf_pink();
const colorf& colorf_plum();
const colorf& colorf_red();
const colorf& colorf_indianred();
const colorf& colorf_mediumvioletred();
const colorf& colorf_orangered();
const colorf& colorf_violetred();
const colorf& colorf_salmon();
const colorf& colorf_sienna();
const colorf& colorf_tan();
const colorf& colorf_thistle();
const colorf& colorf_turquoise();
const colorf& colorf_darkturquoise();
const colorf& colorf_mediumturquoise();
const colorf& colorf_violet();
const colorf& colorf_blueviolet();
const colorf& colorf_wheat();
const colorf& colorf_white();
const colorf& colorf_yellow();
const colorf& colorf_greenyellow();

template <class VEC3>
class line {
public:
  line();
  line(const VEC3&,const VEC3&);
  virtual ~line();
public:
  line(const line&);
  line& operator=(const line&);
public:
  void set_value(const VEC3&,const VEC3&);
  const VEC3& position() const;
  const VEC3& direction() const;
};

class vec2f {
public:
  vec2f();
  vec2f(float,float);
  virtual ~vec2f();
  vec2f(const vec2f&);
  vec2f& operator=(const vec2f&);
public:
  const float& x() const;
  const float& y() const;
  void set_value(const float&,const float&);
  float length() const;
  float normalize();
};
 
class vec3f {
public:
  vec3f();
  vec3f(float,float,float);
  virtual ~vec3f();
  vec3f(const vec3f&);
  vec3f& operator=(const vec3f&);
public:
  const float& x() const;
  const float& y() const;
  const float& z() const;
  void set_value(const float&,const float&,const float&);
  float length() const;
  float normalize();
};
 
class mat4f {
public:
  mat4f();
  virtual ~mat4f();
  mat4f(const mat4f&);
  mat4f& operator=(const mat4f&);
};
 
class rotf {
public:
  rotf();
  rotf(const vec3f&,float);
  rotf(const vec3f&,const vec3f&);
  virtual ~rotf();
  rotf(const rotf&);
  rotf& operator=(const rotf&);
};
 
class box3f {
public:
  box3f();
  virtual ~box3f();
public:
  box3f(const box3f&);
  box3f& operator=(const box3f&);
public:
  void make_empty();
  bool is_empty() const;
  void extend_by(const vec3f&);
  void extend_by(float,float,float);
  const vec3f& mn() const;
  const vec3f& mx() const;
};

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
class vec3d {
public:
  vec3d();
  vec3d(double,double,double);
  virtual ~vec3d();
  vec3d(const vec3d&);
  vec3d& operator=(const vec3d&);
public:
  const double& x() const;
  const double& y() const;
  const double& z() const;
  void set_value(const double&,const double&,const double&);
  double length() const;
  double normalize();
};

class rotd {
public:
  rotd();
  rotd(const vec3d&,double);
  rotd(const vec3d&,const vec3d&);
  virtual ~rotd();
  rotd(const rotd&);
  rotd& operator=(const rotd&);
};

class box3d {
public:
  box3d();
  virtual ~box3d();
public:
  box3d(const box3d&);
  box3d& operator=(const box3d&);
public:
  void make_empty();
  bool is_empty() const;
  void extend_by(const vec3d&);
  void extend_by(double,double,double);
  const vec3d& mn() const;
  const vec3d& mx() const;
};

}

//////////////////////////////////////////////////////////////////////////////
/// sg ///////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

namespace inlib {
namespace sg {

template <class T>
class sf {
public:
  sf();
  virtual ~sf();
  sf(const sf&);
  sf& operator=(const sf&);
public:
  T& value();
  const T& value() const;
  void value(const T&);
};
%extend sf {
  T value_cp() const {return self->value();}
}

template <class T,class TT>
class sf_vec {
public:
  sf_vec();
  virtual ~sf_vec();
  sf_vec(const sf_vec&);
  sf_vec& operator=(const sf_vec&);
public:
  T& value();
  const T& value() const;
  void value(const T&);
};

class sf_string {
public:
  sf_string();
  virtual ~sf_string();
  sf_string(const sf_string&);
  sf_string& operator=(const sf_string&);
public:
  //std_string& value();
  //const std_string& value() const;
  std_string& value();
  const std::string& value() const;
  void value(const std::string&);
};

class sf_vec3f {
public:
  sf_vec3f();
  virtual ~sf_vec3f();
  sf_vec3f(const sf_vec3f&);
  sf_vec3f& operator=(const sf_vec3f&);
public:
  vec3f& value();
  const vec3f& value() const;
  void value(const vec3f&);
};
 
class sf_mat4f {
public:
  sf_mat4f();
  virtual ~sf_mat4f();
  sf_mat4f(const sf_mat4f&);
  sf_mat4f& operator=(const sf_mat4f&);
public:
  mat4f& value();
  const mat4f& value() const;
  void value(const mat4f&);
};
 
class sf_rotf {
public:
  sf_rotf();
  virtual ~sf_rotf();
  sf_rotf(const sf_rotf&);
  sf_rotf& operator=(const sf_rotf&);
public:
  rotf& value();
  const rotf& value() const;
  void value(const rotf&);
};
 
template <class T>
class sf_img {
  sf_img();
  sf_img(const img<T>&);
  virtual ~sf_img();
public:
  sf_img(const sf_img&);
  sf_img& operator=(const sf_img&);
public:
  img<T>& value();
  const img<T>& value() const;
  void value(const img<T>&);
};
 
template <class T>
class sf_enum {
public:
  sf_enum();
  virtual ~sf_enum();
  sf_enum(const sf_enum&);
  sf_enum& operator=(const sf_enum&);
public:
  T& value();
  const T& value() const;
  void value(const T&);
};

template <class T>
class mf {
public:
  mf();
  virtual ~mf();
  mf(const mf&);
  mf& operator=(const mf&);
public:
  size_t size() const;
  bool empty() const;
  const std::vector<T>& values();
  std::vector<T>& values();
};

template <class T,class TT>
class mf_vec {
public:
  mf_vec();
  virtual ~mf_vec();
  mf_vec(const mf_vec&);
  mf_vec& operator=(const mf_vec&);
public:
  size_t size() const;
  bool empty() const;
  const std::vector<T>& values();
  std::vector<T>& values();
};

class mf_string {
public:
  mf_string();
  virtual ~mf_string();
  mf_string(const mf_string&);
  mf_string& operator=(const mf_string&);
public:
  size_t size() const;
  bool empty() const;
  const std::vector<std::string>& values();
  std::vector<std::string>& values();
};

template <class T>
class mf_enum {
public:
  mf_enum();
  virtual ~mf_enum();
  mf_enum(const mf_enum&);
  mf_enum& operator=(const mf_enum&);
public:
  size_t size() const;
  bool empty() const;
  const std::vector<T>& values();
  std::vector<T>& values();
};

}}

%template(sf_bool)       inlib::sg::sf<bool>;
%template(sf_float)      inlib::sg::sf<float>;
%template(sf_vec_colorf) inlib::sg::sf_vec<inlib::colorf,float>;
%template(sf_img_byte)   inlib::sg::sf_img<inlib::byte>;

%template(sf_enum_font_modeling)   inlib::sg::sf_enum<inlib::sg::font_modeling>;
%template(sf_enum_winding_type)    inlib::sg::sf_enum<inlib::sg::winding_type>;
%template(sf_enum_marker_style)    inlib::sg::sf_enum<inlib::sg::marker_style>;
%template(sf_enum_area_style)      inlib::sg::sf_enum<inlib::sg::area_style>;
%template(sf_enum_painting_policy) inlib::sg::sf_enum<inlib::sg::painting_policy>;
%template(sf_enum_hatching_policy) inlib::sg::sf_enum<inlib::sg::hatching_policy>;
%template(sf_enum_projection_type) inlib::sg::sf_enum<inlib::sg::projection_type>;

%template(sf_enum_hjust)           inlib::sg::sf_enum<inlib::sg::hjust>;
%template(sf_enum_vjust)           inlib::sg::sf_enum<inlib::sg::vjust>;

%template(sf_enum_draw_type)       inlib::sg::sf_enum<inlib::sg::draw_type>;
%template(sf_enum_shade_type)      inlib::sg::sf_enum<inlib::sg::shade_type>;

%template(mf_float)            inlib::sg::mf<float>;
%template(mf_vec_vec2f)        inlib::sg::mf_vec<inlib::vec2f,float>;
%template(mf_enum_unit_type)   inlib::sg::mf_enum<inlib::sg::plotter::unit_type>;

%rename(sg_plotter)            inlib::sg::plotter;
%rename(sg_plots)              inlib::sg::plots;
%rename(sg_set_plotter_camera) inlib::sg::set_plotter_camera;
%rename(sg_style_from_res)     inlib::sg::style_from_res;

%include <inlib/sg/enums>

namespace inlib {
namespace sg {

const std::string& font_arialbd_ttf();

const std::string& modeling_boxes();
const std::string& modeling_wire_boxes();
const std::string& modeling_lines();
const std::string& modeling_segments();
const std::string& modeling_points();
const std::string& modeling_top_lines();
const std::string& modeling_texts();
const std::string& modeling_curve();
const std::string& modeling_filled_curve();
const std::string& modeling_bar_chart();
const std::string& modeling_solid();
const std::string& modeling_wire_frame();
const std::string& modeling_reduced_wire_frame();
const std::string& modeling_polygon();
const std::string& modeling_none();
const std::string& modeling_I();
const std::string& modeling_plus();
const std::string& modeling_markers();

typedef unsigned short lpat;

class style {
public:
  sf_vec<colorf,float> color;
  sf_vec<colorf,float> highlight_color;
  sf_vec<colorf,float> back_color;
  sf<float> line_width;
  sf<float> marker_size;
  sf<float> point_size;
  sf<float> font_size;
  sf_enum<sg::font_modeling> font_modeling;
  sf_enum<winding_type> front_face;
  sf<lpat> line_pattern;
  sf_enum<sg::marker_style> marker_style;
  sf_enum<sg::area_style> area_style;
  sf_string modeling; 
  sf_string light_model; 
  sf_string tick_modeling; 
  sf_string encoding; 
  sf<bool> smoothing;
  sf<bool> hinting;
  sf_string cut;
  sf_enum<sg::painting_policy> painting;
  sf_enum<sg::hatching_policy> hatching;
  sf_enum<sg::projection_type> projection;
  sf_string font;
  sf<int> multi_node_limit;
  sf<int> divisions;
  sf<unsigned int> rotation_steps;
  sf<float> spacing;
  sf<float> angle;
  sf<float> scale;
  sf<float> offset;
  sf<float> strip_width;
  sf<bool> visible;
  sf<float> bar_offset;
  sf<float> bar_width;
  sf<bool> editable;
  sf<bool> automated;
  sf_string options;
  sf_string color_mapping;
  sf<bool> enforced;
  sf_vec3f translation;
};

class text_style {
public:
  sf<bool> visible;
  sf_vec<colorf,float> color;
  sf_vec<colorf,float> back_color;
  sf<float> back_shadow;

  sf_string modeling; 
  sf_string font;
  sf<float> font_size;
  sf_enum<sg::font_modeling> font_modeling;
  sf_string encoding; 
  sf<bool> smoothing;
  sf<bool> hinting;
  sf_enum<sg::hjust> hjust;
  sf_enum<sg::vjust> vjust;
  sf<float> scale;
  // For 3D text :
  sf_vec3f x_orientation;
  sf_vec3f y_orientation;
  // For bitmap text :
  sf<bool> rotated;

  // for text_hershey :
  sf<float> line_width;
  sf<lpat> line_pattern;
  sf<bool> enforced;
  sf_vec3f translation;

  // for text_freetype tessellation :
  sf_enum<winding_type> front_face;

  sf_string options; //for gopaw.
};

class render_action {
private:
  render_action();
  virtual ~render_action();
  render_action(const render_action&);
  render_action& operator=(const render_action&);
};

class write_action {
private:
  write_action(std::ostream&);
  virtual ~write_action();
  write_action(const write_action&);
  write_action& operator=(const write_action&);
};

}}

#include "hep.i"

#include "nodes.i"
 
namespace inlib {
namespace sg {

class base_freetype {
private:
  base_freetype();
};

class plottable {
protected:
  plottable();
  virtual ~plottable();
  plottable(const plottable&);
  plottable& operator=(const plottable&);
};

class h1d2plot : public plottable {
public:
  h1d2plot(const histo::h1d&);
  virtual ~h1d2plot();
  h1d2plot(const h1d2plot&);
  h1d2plot& operator=(const h1d2plot&);
};

class h1d2plot_cp : public plottable {
public:
  h1d2plot_cp(const histo::h1d&);
  virtual ~h1d2plot_cp();
  h1d2plot_cp(const h1d2plot_cp&);
  h1d2plot_cp& operator=(const h1d2plot_cp&);
};

%template(sf_enum_shape_type)                  inlib::sg::sf_enum<inlib::sg::plotter::shape_type>;
%template(sf_enum_colormap_axis_labeling_type) inlib::sg::sf_enum<inlib::sg::plotter::colormap_axis_labeling_type>;
 
class plotter : public node {
public:
  virtual node* copy() const;
public:
  sf<float> width;
  sf<float> height;
  sf<float> left_margin;
  sf<float> right_margin;
  sf<float> bottom_margin;
  sf<float> top_margin;
  sf<float> depth;
  sf<float> down_margin;    
  sf<float> up_margin;
  sf<bool> title_up;  
  sf<float> title_to_axis;  
  sf<float> title_height;  
  sf<bool> title_automated;  
  sf_enum<hjust> title_hjust;
  sf_string title; //output if title_automated.
  sf<bool> colormap_visible;
  enum colormap_axis_labeling_type {
    cells = 0,
    min_max
  };
  sf_enum<colormap_axis_labeling_type> colormap_axis_labeling;
  sf<bool> colormap_attached;
  sf<bool> colormap_axis_visible;
  sf<bool> x_axis_enforced;
  sf<bool> x_axis_automated;
  sf<float> x_axis_min;
  sf<float> x_axis_max;
  sf<bool> x_axis_is_log;
  sf<bool> y_axis_enforced;
  sf<bool> y_axis_automated;
  sf<float> y_axis_min;
  sf<float> y_axis_max;
  sf<bool> y_axis_is_log;
  sf<bool> z_axis_enforced;
  sf<bool> z_axis_automated;
  sf<float> z_axis_min;
  sf<float> z_axis_max;
  sf<bool> z_axis_is_log;
  sf<float> value_top_margin;
  sf<float> infos_width;
  sf<float> infos_x_margin;
  sf<float> infos_y_margin;
  sf_string infos_what;
  sf<bool> func2D_borders_visible;  
  sf<float> theta;
  sf<float> phi;
  sf<float> tau;
  sf<bool> legends_automated;
  mf_vec<vec2f,float> legends_origin;
  enum unit_type {
    unit_percent,
    unit_axis
  };
  mf_enum<unit_type> legends_origin_unit;
  mf_vec<vec2f,float> legends_size; //overall legend boxes size.
  mf_string legends_string;
  sf<bool> shape_automated;
  enum shape_type {
    xy = 0,
    xyz
  };
  sf_enum<shape_type> shape;
  sf<float> xy_depth;
  sf<unsigned int> curve_number_of_points;
  sf<bool> data_light_on_automated;
  sf<bool> primitives_enforced;
  sf<bool> inner_frame_enforced;  
  sf<bool> top_axis_visible;  
  sf<bool> right_axis_visible;  
  sf<bool> superpose_bins;
  sf<unsigned int> number_of_levels;
  mf<float> levels;
public:
  plotter(const base_freetype&);
  virtual ~plotter();
  plotter(const plotter&);
  plotter& operator=(const plotter&);
public:
  void add_plottable(plottable*);
  style& bins_style(unsigned int);
  style& points_style(unsigned int);
  style& func_style(unsigned int);
  style& errors_style(unsigned int);
  style& left_hatch_style(unsigned int);
  style& right_hatch_style(unsigned int);
  style& legend_style(unsigned int);
  text_style& infos_style();
  void clear();
  const separator& etc_sep() const;
  separator& etc_sep();
};

%extend plotter {
  void plot(const histo::h1d& a_histo) {self->add_plottable(new inlib::sg::h1d2plot(a_histo));}
  void plot_cp(const histo::h1d& a_histo) {self->add_plottable(new inlib::sg::h1d2plot_cp(a_histo));}
  void plot(const histo::h2d& a_histo) {self->add_plottable(new inlib::sg::h2d2plot(a_histo));}
  void plot_cp(const histo::h2d& a_histo) {self->add_plottable(new inlib::sg::h2d2plot_cp(a_histo));}

  void plot(const histo::p1d& a_histo) {self->add_plottable(new inlib::sg::p1d2plot(a_histo));}
  void plot_cp(const histo::p1d& a_histo) {self->add_plottable(new inlib::sg::p1d2plot_cp(a_histo));}
  //void plot(const histo::p2d& a_histo) {self->add_plottable(new inlib::sg::p2d2plot(a_histo));}
  //void plot_cp(const histo::p2d& a_histo) {self->add_plottable(new inlib::sg::p2d2plot_cp(a_histo));}

  void plot(const histo::c2d& a_cloud) {self->add_plottable(new inlib::sg::c2d2plot(a_cloud));}
  void plot_cp(const histo::c2d& a_cloud) {self->add_plottable(new inlib::sg::c2d2plot_cp(a_cloud));}
  void plot(const histo::c3d& a_cloud) {self->add_plottable(new inlib::sg::c3d2plot(a_cloud));}
  void plot_cp(const histo::c3d& a_cloud) {self->add_plottable(new inlib::sg::c3d2plot_cp(a_cloud));}
}

class plots : public node {
public:
  virtual node* copy() const;
public:
  sf<float> width;
  sf<float> height;
  sf<unsigned int> cols;
  sf<unsigned int> rows;
  sf<bool> view_border;
  sf<float> plotter_scale;
  sf<bool> border_visible;
  sf<float> border_width;
  sf<float> border_height;
  sf_vec<colorf,float> border_color;
  sf<float> left_margin;
  sf<float> right_margin;
  sf<float> top_margin;
  sf<float> bottom_margin;
  sf<float> horizontal_spacing;
  sf<float> vertical_spacing;
public:
  plots(const base_freetype&);
  virtual ~plots();
  plots(const plots&);
  plots& operator=(const plots&);
public:
  plotter& current_plotter();
  unsigned int number() const;
  unsigned int current_index() const;
  void set_regions(unsigned int a_cols=1,unsigned int a_rows=1,bool a_transfer = false);
  void next();
  bool set_current_plotter(unsigned int);
  void adjust_size(unsigned int,unsigned int);
};

void set_plotter_camera(plotter&,ortho&,unsigned int,unsigned int);

class viewer {
public:
  viewer(std::ostream&,unsigned int,unsigned int);
  virtual ~viewer();
  viewer(const viewer&);
  viewer& operator=(const viewer&);
public:
  std::ostream& out() const;
  unsigned int width() const;
  unsigned int height() const;
  group& sg();
  const group& sg() const;
};

viewer* cast_viewer(const std::string&);

class render_manager {
private:
  render_manager();
  virtual ~render_manager();
  render_manager(const render_manager&);
  render_manager& operator=(const render_manager&);
};

}}

#include "offscreen.i"

#include "socket.i"
#include "sg_client.i"

namespace inlib {
namespace sg {
  
class gui_viewer : public viewer {
private:
  gui_viewer(std::ostream&,render_manager&,const base_freetype&,unsigned int,unsigned int,bool);
  virtual ~gui_viewer();
  gui_viewer(const gui_viewer&);
  gui_viewer& operator=(const gui_viewer&);
public:
  const std::string& res_dir() const;
  virtual opener& opener();
  //bool first_data_dir(std::string& a_s) const;
  //bool find_file(const std::string&,std::string&);
public:
  void show_console(const std::string&);
  void hide_console();
  void set_console_size(float = 0.3F,float = 0.05F,float = 1);
  void hide_main_menu();
  void show_main_menu();
  void hide_camera_menu();
  void show_camera_menu();
  bool adapt_camera_to_scene();
  bool set_scene_light_on(bool);
  void toggle_light();
  void set_plane_viewer(bool);
  void hide_meta_zone();
public:
  const selection& scene() const;
  selection& scene();
  const xml::styles& styles() const;
  xml::styles& styles();
  
  void set_scene_camera(base_camera*);
  base_camera* scene_camera() const;

  void set_scene_light(torche*);
public:
  static const std::string& s_default();
};
%extend gui_viewer {
  bool first_data_dir(std_string& a_s) const {return self->first_data_dir(a_s);}
  bool find_file(const std::string& a_what,std_string& a_path) {return self->find_file(a_what,a_path);}
}

gui_viewer* cast_gui_viewer(viewer&);

plots* get_sg_plots(gui_viewer&);

void style_from_res(const xml::styles&,const std::string&,sg::plotter&,bool);
void style_from_res(const gui_viewer&,const std::string&,sg::plotter&); //backcomp
 
}}

//////////////////////////////////////////////////////////////////////////////
/// waxml ////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

%rename(waxml_file)   inlib::waxml::file;

namespace inlib {
namespace waxml {

class file {
public:
  file();
  virtual ~file();
private:
  file(const file&);
  file& operator=(const file&);
public:
  bool open(const std::string&);
  bool close();
  bool write(const histo::h1d&,const std::string&,const std::string&);
  bool write(const histo::h2d&,const std::string&,const std::string&);
  bool write(const histo::h3d&,const std::string&,const std::string&);
  bool write(const histo::p1d&,const std::string&,const std::string&);
  bool write(const histo::p2d&,const std::string&,const std::string&);
};

}}

//////////////////////////////////////////////////////////////////////////////
/// rroot ////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

//%template(leaf_float)      inlib::rroot::leaf<float>;

%rename(rroot_file)          inlib::rroot::file;
%rename(rroot_fac)           inlib::rroot::fac;
%rename(rroot_tree)          inlib::rroot::tree;
%rename(rroot_branch)        inlib::rroot::branch;
%rename(rroot_base_leaf)     inlib::rroot::base_leaf;
%rename(rroot_leaf_int)      inlib::rroot::leaf<int>;
%rename(rroot_leaf_float)    inlib::rroot::leaf<float>;
%rename(rroot_leaf_double)   inlib::rroot::leaf<double>;

%rename(rroot_find_dir)         inlib::rroot::find_dir;
%rename(rroot_read)             inlib::rroot::read;
%rename(rroot_key_to_h1d)       inlib::rroot::key_to_h1d;
%rename(rroot_key_to_tree)      inlib::rroot::key_to_tree;
%rename(rroot_cast_leaf_int)    inlib::rroot::cast_leaf_int;
%rename(rroot_cast_leaf_float)  inlib::rroot::cast_leaf_float;
%rename(rroot_cast_leaf_double) inlib::rroot::cast_leaf_double;

namespace inlib {
namespace rroot {

class ifile {
private:
  ifile();
  virtual ~ifile();
  ifile(const ifile&);
  ifile& operator=(const ifile&);
};

class key {
public:
  key(std::ostream&);
  virtual ~key();
private:
  key(const key&);
  key& operator=(const key&);
public:
};

class ifac {
private:
  ifac();
  virtual ~ifac();
  ifac(const ifac&);
  ifac& operator=(const ifac&);
};

class fac : public ifac {
public:
  fac(std::ostream&);
  virtual ~fac();
  fac(const fac&);
  fac& operator=(const fac&);
public:
};

}}

%template(std_vector_keys)     std::vector<inlib::rroot::key*>;

namespace inlib {
namespace rroot {

class directory {
public:
  directory(ifile&);
  virtual ~directory();
private:
  directory(const directory&);
  directory& operator=(const directory&);
public:
  key* find_key(const std::string&);
  const std::vector<key*>& keys() const;
  std::vector<key*>& keys();
};

class file : public ifile {
public:
  file(std::ostream&,const std::string&,bool);
  virtual ~file();
private:
  file(const file&);
  file& operator=(const file&);
public:
  bool is_open() const;
  void close();
  directory& dir();
  const directory& dir();
};

class TDirectory : public directory {
public:
  TDirectory(ifile&);
  virtual ~TDirectory();
private:
  TDirectory(const TDirectory&);
  TDirectory& operator=(const TDirectory&);
};

%newobject find_dir;
TDirectory* find_dir(directory&,const std::string&);

%newobject key_to_h1d;
histo::h1d* key_to_h1d(ifile&,key&);
void read(std::ostream&,ifile&,const std::vector<key*>&,bool recursive,bool ls,bool dump,unsigned int spaces);

class branch {
public:
  branch(std::ostream&,ifac&);
  virtual ~branch();
private:
  branch(const branch&);
  branch& operator=(const branch&);
//public:
//virtual bool find_entry(ifile&,unsigned int,unsigned int&);
};
%extend branch {
  bool find_entry(ifile& a_file,unsigned int a_entry) {
    unsigned int n;
    return self->find_entry(a_file,a_entry,n);
  }
}

template <class T>
class leaf {
public:
  leaf(std::ostream&,ifac&);
  virtual ~leaf();
private:
  leaf(const leaf&);
  leaf& operator=(const leaf&);
//public:
//bool value(unsigned int,T&);
};
%extend leaf {
  T value(unsigned int a_index) const {
    T v;
    if(!self->value(a_index,v)) {}
    return v;
  }
}

%template(leaf_int)       leaf<int>;
%template(leaf_float)     leaf<float>;
%template(leaf_double)    leaf<double>;

class base_leaf {
private:
  base_leaf(std::ostream&,ifac&);
  virtual ~base_leaf();
  base_leaf(const base_leaf&);
  base_leaf& operator=(const base_leaf&);
public:
  virtual const std::string& s_cls() const;
};

leaf<int>*    cast_leaf_int(base_leaf&);
leaf<float>*  cast_leaf_float(base_leaf&);
leaf<double>* cast_leaf_double(base_leaf&);

class tree {
public:
  tree(ifile&,ifac&);
  virtual ~tree();
private:
  tree(const tree&);
  tree& operator=(const tree&);
public:
  //uint64 entries() const;
  bool show(std::ostream&,unsigned int);
  branch* find_branch(const std::string&,bool=false) const;
  base_leaf* find_leaf(const std::string&,bool=false) const;
  branch* find_leaf_branch(const base_leaf&) const;
};
%extend tree {
  unsigned int entries() const {return (unsigned int)(self->entries());}
}

%newobject key_to_tree;
tree* key_to_tree(ifile&,ifac&,key&);


}}

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
/// sg ///////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

%rename(spark_greet)     inlib::spark::greet;
%rename(spark_get_xyzs)  inlib::spark::get_xyzs;

namespace inlib {
namespace spark {

char const* greet();
void get_xyzs(const std::vector<double>&,const std::vector<double>&,const std::vector<double>&);
 
}}

//exlib_build_use skip
