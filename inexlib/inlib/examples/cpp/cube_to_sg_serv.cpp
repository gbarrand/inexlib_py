// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file inlib.license for terms.

//inlib_build_use socket

#ifdef INLIB_MEM
#include <inlib/mem>
#endif //INLIB_MEM

#include <inlib/net/sg_client>
#include <inlib/sg/send>

#include <inlib/sg/separator>
#include <inlib/sg/rgba>
#include <inlib/sg/cube>

#include <inlib/args>
#include <iostream>

int main(int argc,char** argv) {

#ifdef INLIB_MEM
  inlib::mem::set_check_by_class(true);{
#endif //INLIB_MEM
  inlib::args args(argc,argv);

  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////

  std::string host;
  if(!args.find("-host",host)) {
    std::cout << "argument -host=<string> lacking." << std::endl;
    return EXIT_FAILURE;
  }

  unsigned int port;
  if(!args.find("-port",port)) port = 50800;

  inlib::net::sg_client dc(std::cout,false,true);

  std::cout << "try to connected to"
            << " " << host
            << " " << port
            << "..." << std::endl;

  if(!dc.initialize(host,port)) {
    std::cout << "can't connect to"
              << " " << host
              << " " << port
              << "." << std::endl;
    return EXIT_FAILURE;
  }

  std::cout << "connected to"
            << " " << host
            << " " << port
            << "." << std::endl;

  //////////////////////////////////////////////////////////
  /// create a scene graph : ///////////////////////////////
  //////////////////////////////////////////////////////////

  inlib::sg::separator sep;

  inlib::sg::rgba* col = new inlib::sg::rgba;
  col->color = inlib::colorf_red();
  sep.add(col);

  inlib::sg::cube* cub = new inlib::sg::cube;
  sep.add(cub);

  //////////////////////////////////////////////////////////
  /// send scene graph : ///////////////////////////////////
  //////////////////////////////////////////////////////////

  //::printf("debug : scene_radius %g\n",scene_radius);
  inlib::args opts;
  opts.add(inlib::sg::s_send_placement(),inlib::sg::s_placement_static());
  opts.add(inlib::sg::s_send_radius(),"2");

  if(!inlib::sg::send(dc,sep,0,opts)){
    std::cout << "send() failed." << std::endl;
    return EXIT_FAILURE;
  }

  if(!dc.socket().send_string(inlib::sg::s_protocol_disconnect())) {}
  dc.socket().disconnect();

  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////

#ifdef INLIB_MEM
  }inlib::mem::balance(std::cout);
#endif //INLIB_MEM

  return EXIT_SUCCESS;
}
