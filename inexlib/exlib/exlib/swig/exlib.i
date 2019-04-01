// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
%include inlib.i

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

%rename(fits_image_read_slice_to_img) exlib::fits_image::read_slice_to_img;

namespace exlib {
namespace fits_image {
bool read_slice_to_img(std::ostream&,const std::string& a_fits_file,
                       unsigned int a_hdu,unsigned int a_slice,bool a_yswap,
                       const inlib::lut<double>& a_lut,const inlib::SOPI::cmap& a_cmap,
		       inlib::img<inlib::byte>& a_img);
}}

%rename(xml_load_style_file) exlib::xml::load_style_file;

namespace exlib {
namespace xml {

bool load_style_file(std::ostream&,const std::string&,inlib::xml::styles&);

}}

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
%rename(sg_gl2ps_manager) exlib::sg::gl2ps_manager;
%rename(sg_gl2ps_action)  exlib::sg::gl2ps_action;
%rename(sg_text_freetype) exlib::sg::text_freetype;

namespace exlib {
namespace sg {

class text_freetype : public inlib::sg::base_freetype {
public:
  text_freetype();
  virtual ~text_freetype();
  text_freetype(const text_freetype&);
  text_freetype& operator=(const text_freetype&);
};

class gl2ps_manager {
public:
  gl2ps_manager();
  virtual ~gl2ps_manager(){}
private:
  gl2ps_manager(const gl2ps_manager&);
  gl2ps_manager& operator=(const gl2ps_manager&);
};

class gl2ps_action : public inlib::sg::render_action {
public:
  gl2ps_action(gl2ps_manager&,std::ostream&,unsigned int,unsigned int);
  virtual ~gl2ps_action(){}
private:
  gl2ps_action(const gl2ps_action&);
  gl2ps_action& operator=(const gl2ps_action&);
public:
  bool open(const std::string&);
  bool close();
};

}}

namespace inlib {
namespace net {

%extend sg_client {
  bool send_sg(sg::node& a_node,const args& a_args) {
    return inlib::sg::send(*self,a_node,exlib::compress_buffer,a_args);
  }
}

}}

%rename(sg_write_paper) exlib::sg::write_paper;

namespace exlib {
namespace sg {

bool write_paper(std::ostream& a_out,gl2ps_manager& a_gl2ps_mgr,inlib::sg::zb_manager& a_zb_mgr,
                 float a_back_r,float a_back_g,float a_back_b,float a_back_a,
                 inlib::sg::node& a_scene_graph,
                 unsigned int a_width,unsigned int a_height,
		 const std::string& a_file,const std::string& a_format);

}}

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

//exlib_build_use skip
