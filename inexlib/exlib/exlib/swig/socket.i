// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

%rename(net_inet_socket)        inlib::net::inet_socket;
%rename(net_serror)             inlib::net::serror;
%rename(net_herror)             inlib::net::herror;

namespace inlib {
namespace net {

std::string serror();
 
class base_socket {
public:
  virtual void disconnect() = 0;
public:
  base_socket(std::ostream&,bool);
  virtual ~base_socket();
protected:
  base_socket(const base_socket&);
  base_socket& operator=(const base_socket&);
public:
  bool verbose() const;
  void set_verbose(bool);
  bool is_connected() const;
  //SOCKET socket() const {return m_socket;}
  std::ostream& out() const;
  void close();
public:
  //bool send_buffer(const char* a_buffer,uint64 a_length,uint64 a_BLOCK = 65536);
  //bool fetch_buffer(char* a_buffer,uint64 a_length,uint64 a_BLOCK = 65536);
  //bool fetch_upto_char(char a_char,char*& a_buffer,uint64& a_length,unsigned int a_BLOCK = 65536);
  //bool fetch_one_shoot(char*& a_buffer,uint64& a_length,unsigned int a_BLOCK = 65536);
  //bool fetch_upto_end(char*& a_buffer,uint64& a_length,unsigned int a_BLOCK = 65536);
  //bool fetch_upto_end(FILE* a_FILE,uint64& a_length,unsigned int a_BLOCK = 65536);
  /*
  template <class T>
  bool send(const T& a_value) {
    char buffer[sizeof(T)];
    write_buffer<T>(a_value,buffer);
    return send_buffer(buffer,sizeof(T));
  }

  template <class T>
  bool fetch(T& a_value) {
    char buffer[sizeof(T)];
    if(!fetch_buffer(buffer,sizeof(T))) return false;
    read_buffer<T>(buffer,a_value);
    return true;
  }
  */
  bool send_uchar(unsigned char a_value);
  //bool fetch_uchar(unsigned char& a_value);
  bool send_bool(bool a_value);
  bool fetch_bool(bool& a_value);
  bool send_string(const std::string& a_string);
  //bool fetch_string(std::string& a_string);
  bool send_text(const std::vector<std::string>& a_text);
  //bool fetch_text(std::vector<std::string>& a_text);
  bool send_file(const std::string& a_file);
  bool fetch_file(const std::string& a_file);
  //bool is_there_input(bool& a_is,unsigned int a_micro_secs = 10);
  bool is_active(unsigned int a_micro_secs = 10);
};
  
std::string herror();
 
class inet_socket : public base_socket {
public: //base_socket        
  virtual void disconnect();
public:
  inet_socket(std::ostream&,bool a_verbose = false);
  virtual ~inet_socket();
protected:
  inet_socket(const inet_socket& a_from);
  inet_socket& operator=(const inet_socket&);
public:
  bool bind(const std::string& a_host,unsigned int a_port,unsigned int a_max_trial,unsigned int a_secs,bool a_reuse_addr);
  void set_dump_ECONNABORTED(bool);
  //bool accept(SOCKET a_socket,bool a_blocking);
  bool bind_accept(const std::string& a_host,unsigned int a_port,
                   unsigned int a_max_trial,unsigned int a_secs,
                   bool a_reuse_addr,bool a_blocking);
  bool connect(const std::string& a_host,unsigned int a_port,
               unsigned int a_select_secs,unsigned int a_max_trial,unsigned int a_secs);
};
    
}}

namespace inlib {
bool net_host_name(std::ostream&,std_string&);  //use inlib.std_string for the second arg.
bool net_inet_sip(std::ostream&,const std::string&,std_string&);  //use inlib.std_string for the second arg.
}

  
/* the below induces duplicate symbols when linking exlib/apps/rspy.cpp :
%inline {
namespace inlib {
  bool net_host_name(std::ostream& a_out,std_string& a_host) {return net::host_name(a_out,a_host);} //std_string& and not std::string&.
  bool net_inet_sip(std::ostream& a_out,const std::string& a_host,std_string& a_sip) {return net::inet_sip(a_out,a_host,a_sip);}
}  
}
*/

//exlib_build_use skip
