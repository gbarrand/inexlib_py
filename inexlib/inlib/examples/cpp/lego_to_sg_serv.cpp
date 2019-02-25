// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file inlib.license for terms.

//inlib_build_use socket

#ifdef INLIB_MEM
#include <inlib/mem>
#endif //INLIB_MEM

#include <inlib/net/sg_client>
#include <inlib/sg/send>

#include <inlib/random>
#include <inlib/sg/h2plot>

#include <inlib/sg/plotter>
#include <inlib/sg/set_plotter_camera>

//#include <exlib/sg/text_freetype>
#include <inlib/sg/dummy_freetype>

#include <inlib/args>
#include <iostream>
#include <cstdlib>

int main(int argc,char** argv) {

#ifdef INLIB_MEM
  inlib::mem::set_check_by_class(true);{
#endif

  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  inlib::args args(argc,argv);

  std::string host;
  if(!args.find("-host",host)) {
    std::cout << "argument -host=<string> lacking." << std::endl;
    return EXIT_FAILURE;
  }

  unsigned int port;
  if(!args.find("-port",port)) port = 50800;

  inlib::net::sg_client dc(std::cout,false,true);

  std::cout << "try to connected to " << host << " " << port << "..." << std::endl;

  if(!dc.initialize(host,port)) {
    std::cout << "can't connect to " << host << " " << port << "." << std::endl;
    return EXIT_FAILURE;
  }

  std::cout << "connected to " << host << " " << port << "." << std::endl;

  //////////////////////////////////////////////////////////
  /// create and fill histogram : //////////////////////////
  //////////////////////////////////////////////////////////
  unsigned int entries = 10000;

  inlib::random::gauss rg(1,2);
  inlib::random::bw rbw(0,1);
  //inlib::histo::h2d h("Gauss_BW",100,-5,5,100,-2,2);
  inlib::histo::h2d h("Gauss_BW",20,-5,5,20,-2,2);
  for(unsigned int count=0;count<entries;count++) h.fill(rg.shoot(),rbw.shoot(),0.8);

  //////////////////////////////////////////////////////////
  /// create scene graph ///////////////////////////////////
  /// create the plotter ///////////////////////////////////
  /// declare the histo to the plotter /////////////////////
  //////////////////////////////////////////////////////////
  inlib::sg::separator* sep = new inlib::sg::separator;

  //exlib::sg::text_freetype ttf;
  inlib::sg::dummy_freetype ttf;
  inlib::sg::plotter* plotter = new inlib::sg::plotter(ttf);

  //WARNING : we give ownership of h1d2plot to the plotter,
  //          but we still have ownership of the h histo.
  plotter->add_plottable(new inlib::sg::h2d2plot(h));

  plotter->bins_style(0).color = inlib::colorf_grey();
  plotter->bins_style(0).modeling = inlib::sg::modeling_boxes();
  plotter->bins_style(0).painting = inlib::sg::painting_violet_to_red;

  //plotter->infos_style().font = inlib::sg::font_arialbd_ttf();
  //plotter->infos_style().front_face = inlib::sg::winding_cw;
  plotter->infos_style().font = inlib::sg::font_hershey();
  plotter->infos_x_margin = 0.01f; //percent of plotter width.
  plotter->infos_y_margin = 0.01f; //percent of plotter height.

  plotter->shape = inlib::sg::plotter::xyz;
  plotter->shape_automated = false;

  sep->add(plotter);

  //////////////////////////////////////////////////////////
  /// send scene graph : ///////////////////////////////////
  //////////////////////////////////////////////////////////

  //::printf("debug : scene_radius %g\n",scene_radius);
  inlib::args opts;
  opts.add(inlib::sg::s_send_placement(),inlib::sg::s_placement_static());

  if(!inlib::sg::send(dc,*sep,0,opts)){
    std::cout << "send() failed." << std::endl;
    return EXIT_FAILURE;
  }

  if(!dc.socket().send_string(inlib::sg::s_protocol_disconnect())) {}
  dc.socket().disconnect();

  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////

  delete sep;
  
#ifdef INLIB_MEM
  }inlib::mem::balance(std::cout);
#endif

  return EXIT_SUCCESS;
}
