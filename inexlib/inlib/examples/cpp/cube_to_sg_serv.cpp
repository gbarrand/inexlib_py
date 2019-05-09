// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file inlib.license for terms.

//inlib_build_use socket

#ifdef INLIB_MEM
#include <inlib/mem>
#endif //INLIB_MEM

#include <inlib/net/sg_client>
#include <inlib/sg/send>

#include <inlib/sg/separator>
#include <inlib/sg/matrix>
#include <inlib/sg/rgba>
#include <inlib/sg/cube>

#include <inlib/sys/sleep>

#include <inlib/args>
#include <iostream>

int main(int argc,char** argv) {

#ifdef INLIB_MEM
  inlib::mem::set_check_by_class(true);{
#endif //INLIB_MEM
  inlib::args args(argc,argv);

  //////////////////////////////////////////////////////////
  /// args : ///////////////////////////////////////////////
  //////////////////////////////////////////////////////////

  if(args.is_arg("-h")) {
    std::cout << "-verbose" << std::endl;
    std::cout << "-host=<string>  : computer on which sg_serv is running." << std::endl;
    std::cout << "-port=<uint>    : port on which sg_serv is listening." << std::endl;
    std::cout << "-secs=<uint>    : seconds to sleep between each sending." << std::endl;
    std::cout << "-red            : send red cube only." << std::endl;
    std::cout << "-blue           : send blue cube only." << std::endl;
    std::cout << "-numbers=<uint> : to loop on sending." << std::endl;
    return EXIT_SUCCESS;
  }
  
  bool verbose = args.is_arg("-verbose");
  
  std::string host;
  if(!args.find("-host",host)) {
    std::cout << "argument -host=<string> lacking." << std::endl;
    return EXIT_FAILURE;
  }

  unsigned int port;
  args.find<unsigned int>("-port",port,50800);

  unsigned int secs;
  args.find<unsigned int>("-secs",secs,3);

  unsigned int numbers;
  args.find<unsigned int>("-numbers",numbers,1);

  bool send_blue = true;
  bool send_red = true;
  
  if(args.is_arg("-red"))  send_blue = false;
  if(args.is_arg("-blue")) send_red = false;

  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  
  inlib::net::sg_client dc(std::cout,false,true);

  if(verbose) std::cout << "try to connected sg_client to sg_serv on " << inlib::sout(host) << " with port " << port << "..." << std::endl;

  if(!dc.initialize(host,port)) {
    std::cout << "can't connect to"
              << " " << host
              << " " << port
              << "." << std::endl;
    return EXIT_FAILURE;
  }

  if(verbose) std::cout << "sg_client connected to " << inlib::sout(host) << " " << port << "." << std::endl;

  //////////////////////////////////////////////////////////
  /// create a scene graph : ///////////////////////////////
  //////////////////////////////////////////////////////////

  inlib::sg::separator sep;

  inlib::sg::rgba* col = new inlib::sg::rgba;
  col->color = inlib::colorf_red();
  sep.add(col);

  inlib::sg::matrix* mtx = new inlib::sg::matrix;
  mtx->set_translate(-1,0,0);
  sep.add(mtx);
  
  inlib::sg::cube* cub = new inlib::sg::cube;
  sep.add(cub);

  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  for(size_t count=0;count<numbers;count++) {
  
  //////////////////////////////////////////////////////////
  /// send scene graph : ///////////////////////////////////
  //////////////////////////////////////////////////////////
  if(verbose) std::cout << "send clear static sg..." << std::endl;
  if(!dc.send_string(inlib::sg::s_protocol_clear_static_sg())){
    std::cout << "send() failed." << std::endl;
    return EXIT_FAILURE;
  }

  if(verbose) std::cout << "sleep (" << secs << " secs)..." << std::endl;
  inlib::sleep_secs(secs);
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////

  inlib::args opts;
  opts.add(inlib::sg::s_send_placement(),inlib::sg::s_placement_static());
  opts.add(inlib::sg::s_send_radius(),"2");

  if(send_red) {
    if(verbose) std::cout << "send red cube..." << std::endl;
    col->color = inlib::colorf_red();
    mtx->set_translate(-1,0,0);
    if(!inlib::sg::send(dc,sep,0,opts)){
      std::cout << "send() failed." << std::endl;
      return EXIT_FAILURE;
    }
    if(verbose) std::cout << "sleep..." << std::endl;
    inlib::sleep_secs(secs);
  }
  

  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  
  if(send_blue) {
    if(verbose) std::cout << "send blue cube..." << std::endl;
    col->color = inlib::colorf_blue();
    mtx->set_translate(1,0,0);
    if(!inlib::sg::send(dc,sep,0,opts)){
      std::cout << "send() failed." << std::endl;
      return EXIT_FAILURE;
    }
    if(verbose) std::cout << "sleep..." << std::endl;
    inlib::sleep_secs(secs);
  }
  
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////

  } //count

  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  if(verbose) std::cout << "send disconnect..." << std::endl;
  if(!dc.socket().send_string(inlib::sg::s_protocol_disconnect())) {}
  dc.socket().disconnect();

  if(verbose) std::cout << "sleep..." << std::endl;
  inlib::sleep_secs(secs);
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////

#ifdef INLIB_MEM
  }inlib::mem::balance(std::cout);
  std::cout << "exit(mem) ..." << std::endl;
#else  
  if(verbose) std::cout << "exit ..." << std::endl;
#endif //INLIB_MEM

  return EXIT_SUCCESS;
}
