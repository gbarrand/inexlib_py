// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

%rename(net_sg_client)        inlib::net::sg_client;

namespace inlib {
namespace net {

class sg_client {
public:
  sg_client(std::ostream&,bool,bool);
  virtual ~sg_client();
protected:
  sg_client(const sg_client&);
  sg_client& operator=(const sg_client&);
public:
  bool is_connected() const;
  net::inet_socket& socket();
  std::ostream& out() const;
  bool initialize(const std::string&,unsigned int);
  bool steer();
  bool poll();

  //bool send_buffer_doc(uint64,uint64,const char*,const args&);
  bool send_string(const std::string&);
public:
  bool get_sg_serv_params(std::string&);
};

}}

%rename(sg_s_send_placement)      inlib::sg::s_send_placement;
%rename(sg_s_placement_static)    inlib::sg::s_placement_static;
%rename(sg_s_placement_dynamic)   inlib::sg::s_placement_dynamic;
%rename(sg_s_placement_screen)    inlib::sg::s_placement_screen;
%rename(sg_s_send_radius)         inlib::sg::s_send_radius;
%rename(sg_s_send_scale)          inlib::sg::s_send_scale;
%rename(sg_s_send_clear)          inlib::sg::s_send_clear;

namespace inlib {
namespace sg {
const std::string& s_send_placement();
const std::string& s_placement_static();
const std::string& s_placement_dynamic();
const std::string& s_placement_screen();
const std::string& s_send_radius();
const std::string& s_send_scale();
const std::string& s_send_clear();
}}

%rename(sg_s_protocol_start)             inlib::sg::s_protocol_start;
%rename(sg_s_protocol_disconnect)        inlib::sg::s_protocol_disconnect;
%rename(sg_s_protocol_zdoc)              inlib::sg::s_protocol_zdoc;
%rename(sg_s_protocol_arg_sep)           inlib::sg::s_protocol_arg_sep;

%rename(sg_s_protocol_clear_static_sg)   inlib::sg::s_protocol_clear_static_sg;
%rename(sg_s_protocol_clear_dynamic_sg)  inlib::sg::s_protocol_clear_dynamic_sg;
%rename(sg_s_protocol_clear_screen_sg)   inlib::sg::s_protocol_clear_screen_sg;

namespace inlib {
namespace sg {

const std::string& s_protocol_start();
const std::string& s_protocol_disconnect();
const std::string& s_protocol_zdoc();
const std::string& s_protocol_arg_sep();

const std::string& s_protocol_clear_static_sg();
const std::string& s_protocol_clear_dynamic_sg();
const std::string& s_protocol_clear_screen_sg();

}}

//exlib_build_use skip
