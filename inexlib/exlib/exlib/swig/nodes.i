// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

%rename(sg_node)        inlib::sg::node;
%rename(sg_group)       inlib::sg::group;
%rename(sg_separator)   inlib::sg::separator;
%rename(sg_selection)   inlib::sg::selection;
%rename(sg_base_camera) inlib::sg::base_camera;
%rename(sg_ortho)       inlib::sg::ortho;
%rename(sg_perspective) inlib::sg::perspective;
%rename(sg_frustum)     inlib::sg::frustum;
%rename(sg_lrbt)        inlib::sg::lrbt;
%rename(sg_rgba)        inlib::sg::rgba;
%rename(sg_base_tex)    inlib::sg::base_tex;
%rename(sg_tex_rect)    inlib::sg::tex_rect;
%rename(sg_torche)      inlib::sg::torche;
%rename(sg_head_light)  inlib::sg::head_light;
%rename(sg_matrix)      inlib::sg::matrix;
%rename(sg_polyhedron)  inlib::sg::polyhedron;
%rename(sg_cube)        inlib::sg::cube;
%rename(sg_cone_hat)    inlib::sg::cone_hat;
%rename(sg_blend)       inlib::sg::blend;

%rename(sg_sphere)        inlib::sg::sphere;

%rename(sg_vertices)      inlib::sg::vertices;
%rename(sg_atb_vertices)  inlib::sg::atb_vertices;

%rename(sg_draw_style)    inlib::sg::draw_style;
%rename(sg_shade_model)   inlib::sg::shade_model;

%rename(sg_cast_ortho)       inlib::sg::cast_ortho;
%rename(sg_cast_perspective) inlib::sg::cast_perspective;
%rename(sg_cast_frustum)     inlib::sg::cast_frustum;
%rename(sg_cast_lrbt)        inlib::sg::cast_lrbt;

namespace inlib {
namespace sg {

class node {
public:
  virtual node* copy() const = 0;
public:
  node();
  virtual ~node();
  node(const node&);
  node& operator=(const node&);
public:
  virtual void render(render_action&);
  virtual void write(write_action&);
};

class group : public node {
public:
  virtual node* copy() const;
public:
  group();
  virtual ~group();
  group(const group&);
  group& operator=(const group&);
public:
  void add(node*);
  bool remove(node*);
  bool remove_index(unsigned int);
};

class separator : public group {
public:
  separator();
  virtual ~separator();
  separator(const separator&);
  separator& operator=(const separator&);
};

class selection : public separator {
public:
  selection();
  virtual ~selection();
  selection(const selection&);
  selection& operator=(const selection&);
};

class base_camera : public node {
public:
  virtual float near_height() const = 0;
  virtual void zoom(float) = 0;
public:
  virtual node* copy() const;
public:
  base_camera();
  virtual ~base_camera();
  base_camera(const base_camera&);
  base_camera& operator=(const base_camera&);
public:
  sf<float> znear;
  sf<float> zfar;
  sf_vec3f position;
  sf_rotf orientation;
  sf<float> dx;
  sf<float> da;
  sf<float> ds;
  sf<float> focal;
};

class ortho : public base_camera {
public:
  virtual float near_height() const;
  virtual void zoom(float);
  virtual node* copy() const;
public:  
  ortho();
  virtual ~ortho();
  ortho(const ortho&);
  ortho& operator=(const ortho&);
public:  
  sf<float> height;
};

ortho* cast_ortho(base_camera&);

class perspective : public base_camera {
public:
  virtual float near_height() const;
  virtual void zoom(float);
  virtual node* copy() const;
public:  
  perspective();
  virtual ~perspective();
  perspective(const perspective&);
  perspective& operator=(const perspective&);
public:  
  sf<float> height_angle;
};

perspective* cast_perspective(base_camera&);

class frustum : public base_camera {
public:
  virtual float near_height() const;
  virtual void zoom(float);
  virtual node* copy() const;
public:  
  frustum();
  virtual ~frustum();
  frustum(const frustum&);
  frustum& operator=(const frustum&);
public:  
  sf<float> left;
  sf<float> right;
  sf<float> bottom;
  sf<float> top;
};

frustum* cast_frustum(base_camera&);

class lrbt : public base_camera {
public:
  virtual float near_height() const;
  virtual void zoom(float);
  virtual node* copy() const;
public:  
  lrbt();
  virtual ~lrbt();
  lrbt(const lrbt&);
  lrbt& operator=(const lrbt&);
public:  
  sf<float> left;
  sf<float> right;
  sf<float> bottom;
  sf<float> top;
};

lrbt* cast_lrbt(base_camera&);

class rgba : public node {
public:
  virtual node* copy() const;
public:
  rgba();
  virtual ~rgba();
  rgba(const rgba&);
  rgba& operator=(const rgba&);
public:
  sf_vec<colorf,float> color;
};

class base_tex {
public:
  base_tex();
  virtual ~base_tex();
  base_tex(const base_tex&);
  base_tex& operator=(const base_tex&);
public:
  enum intersect_type {
    intersect_down,
    intersect_move,
    intersect_up
  };
  virtual bool intersect_value(std::ostream&,intersect_type,const line<vec3f>&,std::string&) const = 0;
public:
  sf_img<inlib::byte> img;
  sf_vec<colorf,float> back_color;
  sf<bool> expand;
  sf<unsigned int> limit;
  sf<bool> nearest;
};

class tex_rect : public base_tex, public node {
public:
  virtual bool intersect_value(std::ostream&,intersect_type,const line<vec3f>&,std::string&) const;
  virtual node* copy() const;
public:
  tex_rect();
  virtual ~tex_rect();
  tex_rect(const tex_rect&);
  tex_rect& operator=(const tex_rect&);
};

class torche : public node {
public:
  virtual node* copy() const;
public:
  torche();
  virtual ~torche();
  torche(const torche&);
  torche& operator=(const torche&);
public:
  sf_vec<colorf,float> color;
  sf_vec3f direction;
  sf<bool> on;
};

class head_light : public torche {
public:
  virtual node* copy() const;
public:
  head_light();
  virtual ~head_light();
  head_light(const head_light&);
  head_light& operator=(const head_light&);
};

class blend : public node {
public:
  virtual node* copy() const;
public:
  blend();
  virtual ~blend();
  blend(const blend&);
  blend& operator=(const blend&);
public:
  sf<bool> on;
};

class matrix : public node {
public:
  virtual node* copy() const;
public:
  matrix();
  virtual ~matrix();
  matrix(const matrix&);
  matrix& operator=(const matrix&);
public:
  sf_mat4f mtx;
public:
  void set_identity();
  void set_translate(float,float,float);
  void set_translate(const vec3f&);
  void set_scale(float a_x,float a_y,float a_z);
  void set_scale(float a_s);
  void set_rotate(float a_x,float a_y,float a_z,float a_angle);
  void set_rotate(const vec3f& a_v,float a_angle);
  void mul_mtx(const mat4f& a_m);
  void mul_translate(float a_x,float a_y,float a_z);
  void mul_translate(const vec3f& a_v);
  void mul_scale(float a_x,float a_y,float a_z);
  void mul_scale(float a_s);
  void mul_rotate(float a_x,float a_y,float a_z,float a_angle);
  void mul_rotate(const vec3f& a_v,float a_angle);
  void left_mul_rotate(float a_x,float a_y,float a_z,float a_angle);
  void left_mul_scale(float a_x,float a_y,float a_z);
  void left_mul_translate(float a_x,float a_y,float a_z);
  void left_mul_translate(const vec3f& a_v);
  bool mul_rotate(const vec3f& a_from,const vec3f& a_to);
};

class polyhedron : public node {
public:
  virtual node* copy() const;
public:
  polyhedron();
  virtual ~polyhedron();
  polyhedron(const polyhedron&);
  polyhedron& operator=(const polyhedron&);
public:
  inlib::hep::sf_polyhedron ph;
  sf<bool> solid;
  sf<bool> reduced_wire_frame;
  sf<bool> enforce_edges;
};

class cone_hat : public node {
public:
  virtual node* copy() const;
public:
  cone_hat();
  virtual ~cone_hat();
  cone_hat(const cone_hat&);
  cone_hat& operator=(const cone_hat&);
public:
  sf<float> height;
  sf<float> rmin;
  sf<float> rmax;
  sf<float> angle; //rad
  sf<unsigned int> steps;
};

class cube : public node {
public:
  virtual node* copy() const;
public:
  cube();
  virtual ~cube();
  cube(const cube&);
  cube& operator=(const cube&);
public:  
  sf<float> width;
  sf<float> height;
  sf<float> depth;
};

class sphere : public node {
public:
  virtual node* copy() const;
public:
  sphere();
  virtual ~sphere();
  sphere(const sphere&);
  sphere& operator=(const sphere&);
public:  
  sf<float> radius;
  sf<unsigned int> slices;
  sf<unsigned int> stacks;
};

/* use also inlib/apps/node2swig.cpp program to produce swig code.
class xxx : public node {
public:
  virtual node* copy() const;
public:
  xxx();
  virtual ~xxx();
  xxx(const xxx&);
  xxx& operator=(const xxx&);
};
*/

class draw_style : public node {
public:
  virtual node* copy() const;
public:
  draw_style();
  virtual ~draw_style();
  draw_style(const draw_style&);
  draw_style& operator=(const draw_style&);
public:  
  sf_enum<sg::draw_type> style;
  sf<float> line_width;
  sf<lpat> line_pattern;
  sf<float> point_size;
  sf<bool> cull_face;
  sf<bool> winding_ccw;
};

class shade_model : public node {
public:
  virtual node* copy() const;
public:
  shade_model();
  virtual ~shade_model();
  shade_model(const shade_model&);
  shade_model& operator=(const shade_model&);
public:  
  sf_enum<sg::shade_type> model;
};

}}

namespace inlib {
namespace gl {
typedef unsigned char mode_t;
 
mode_t points();
mode_t lines();
mode_t line_loop();
mode_t line_strip();
mode_t triangles();
mode_t triangle_strip();
mode_t triangle_fan();
bool is_mode(mode_t);
bool is_line(mode_t);
}}

%template(sf_mode_t)       inlib::sg::sf<inlib::gl::mode_t>;

namespace inlib {
namespace sg {
  
class vertices : public node {
public:
  virtual node* copy() const;
public:
  vertices();
  virtual ~vertices();
  vertices(const vertices&);
  vertices& operator=(const vertices&);
public:  
  sf<gl::mode_t> mode;
  mf<float> xyzs;
public:  
  template <class VEC> void add(const VEC&);
  void add(float,float,float);
  size_t number() const;
  void clear();
  bool add_dashed_line(float a_bx,float a_by,float a_bz,
                       float a_ex,float a_ey,float a_ez,
                       unsigned int a_num_dash);
  bool center();
};
 
class atb_vertices : public vertices {
public:
  virtual node* copy() const;
public:
  atb_vertices();
  virtual ~atb_vertices();
  atb_vertices(const atb_vertices&);
  atb_vertices& operator=(const atb_vertices&);
public:
  mf<float> rgbas;
  mf<float> nms;
  sf<bool> do_back;
  sf<float> epsilon;
  sf<bool> draw_edges;
public:  
  void add_pos_color(float a_x,float a_y,float a_z,float a_r,float a_g,float a_b,float a_a);
  template <class VEC,class COLOR>
  void add_pos_color(const VEC& a_pos,const COLOR& a_col);
  template <class VEC,class COLOR>
  void add_pos_color_normal(const VEC& a_pos,const COLOR& a_col,const VEC& a_nm);
  void add_rgba(float a_r,float a_g,float a_b,float a_a);
  void add_color(const colorf& a_col);
  void add_normal(float a_x,float a_y,float a_z);
  template <class VEC>
  void add_normal(const VEC& a_nm);
  template <class VEC>
  void add_pos_normal(const VEC& a_pos,const VEC& a_nm);
  bool add_dashed_line_rgba(float a_bx,float a_by,float a_bz,
                            float a_ex,float a_ey,float a_ez,
                            unsigned int a_num_dash,
                            float a_r,float a_g,float a_b,float a_a);
  void clear();
};
 
}}

//exlib_build_use skip
