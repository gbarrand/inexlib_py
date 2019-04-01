// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

namespace inlib {

class wps {
public:
  wps(std::ostream&);
  virtual ~wps();
private:
  wps(const wps& a_from):m_out(a_from.m_out){}
  wps& operator=(const wps&){return *this;}
public:
  bool open_file(const std::string&,bool = false);
  bool close_file();
  void PS_PAGE_SCALE(float,float,bool a_portrait = true);
  void PS_SCALE(float,float);
  void PS_TRANSLATE(float,float);
  void PS_ROTATE(float);
  void PS_SAVE();
  void PS_RESTORE();
  void PS_BEGIN_PAGE();
  void PS_END_PAGE();
};
}

%rename(zb_buffer)        inlib::zb::buffer;

namespace inlib {
namespace zb {
class buffer {
public:
  typedef unsigned int ZPixel; 
public:
  buffer();
  virtual ~buffer();
protected:  
  buffer(const buffer&);
  buffer& operator=(const buffer&);
public:  
  void clear_color_buffer(ZPixel);
  void clear_depth_buffer();
};
}}
 
%rename(sg_zb_manager)     inlib::sg::zb_manager;
%rename(sg_zb_action)      inlib::sg::zb_action;

namespace inlib {
namespace sg {

class zb_manager : public render_manager {
public:
  zb_manager();
  virtual ~zb_manager();
  zb_manager(const zb_manager&);
  zb_manager& operator=(const zb_manager&);
};

class zb_action : public render_action {
public:
  zb_action(zb_manager&,std::ostream&,unsigned int,unsigned int);
  virtual ~zb_action();
protected:  
  zb_action(const zb_action&);
  zb_action& operator=(const zb_action&);
public:  
  void reset();
  const zb::buffer& zbuffer() const;
  zb::buffer& zbuffer();
  zb::buffer::ZPixel add_color(float,float,float,float);
  zb::buffer::ZPixel add_color(float,float,float);
};

}}

%extend inlib::wps {
  void PS_IMAGE(const inlib::sg::zb_action& a_action){
    self->PS_IMAGE(a_action.ww(),a_action.wh(),inlib::wps::rgb_4,inlib::sg::zb_action::get_rgb,(void*)&a_action);
  }    
}

%rename(sg_write_bsg)      inlib::sg::write_bsg;

namespace inlib {
namespace sg {

class write_bsg : public write_action {
 public:  
  virtual unsigned int protocol() const;
public:
  write_bsg(std::ostream&);
  virtual ~write_bsg();
protected:  
  write_bsg(const write_bsg&);
  write_bsg& operator=(const write_bsg&);
public:  
  bool open_buffer();
  bool close_buffer();
  bool write_file(const std::string&) const;
};

}}

//exlib_build_use skip
