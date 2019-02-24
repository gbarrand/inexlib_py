import inlib
import base_plots
import exlib_offscreen as exlib
import os

class plotter(base_plots.base_plots):
  m_dc = None
  m_ttf = None
  m_sep = None
  m_blend = None
  m_plots = None
  
  def __del__(self):
    del self.m_ttf
    del self.m_sep
    if self.m_dc.send_string(inlib.sg_s_protocol_disconnect()) == False:
      print("inexlib_client.plotter : send protocol_s_disconnect() failed.")
      return
    self.m_dc.socket().disconnect()
    
  def __init__(self,a_out,a_cols,a_rows,a_host,a_port,a_style_file):
    #//////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////
    inlib.env_append_path('EXLIB_FONT_PATH','./res')    
    inlib.env_append_path('EXLIB_FONT_PATH','../res')    

    self.m_ttf = exlib.sg_text_freetype()

    #//////////////////////////////////////////////////////////
    #/// scene graph : ////////////////////////////////////////
    #//////////////////////////////////////////////////////////
    self.m_sep = inlib.sg_separator()
  
    self.m_blend = inlib.sg_blend()
    self.m_blend.thisown = 0
    self.m_sep.add(self.m_blend)

    self.m_plots = inlib.sg_plots(self.m_ttf)
    self.m_plots.thisown = 0
    self.m_plots.set_regions(a_cols,a_rows)
    self.m_sep.add(self.m_plots)

    base_plots.base_plots.__init__(self,a_out,self.m_plots)
    
    if inlib.file_exists(a_style_file) == False:
      print("inexlib_client.plotter : "+a_style_file+" not found.")
    else:
      exlib.xml_load_style_file(a_out,a_style_file,self.m_styles)
    
    #//////////////////////////////////////////////////////////
    #/// net_sg_client : //////////////////////////////////////
    #//////////////////////////////////////////////////////////
    self.m_dc = exlib.net_sg_client(a_out,False,True)  #False=quiet, True=warn if receiving unknown protocol.
    #print("inexlib_client.plotter : try to connected to "+a_host+" "+str(a_port)+" ...")
    if self.m_dc.initialize(a_host,a_port) == False:
      print("inexlib_client.plotter : can't connect to "+a_host+" "+str(a_port))
      return
    #print("inexlib_client.plotter : connected to "+a_host+" "+str(a_port))

  def send_clear_static_scene(self):
    if self.m_dc.send_string(inlib.sg_s_protocol_clear_static_sg()) == False:
      print("inexlib_client.plotter.clear_static_scene : send protocol_s_rwc_clear_static_scene() failed.")
      return False
    return True
    
  def send_plots(self):
    opts = inlib.args()
    opts.add(inlib.sg_s_send_placement(),inlib.sg_s_placement_static())
    if self.m_dc.send_sg(self.m_sep,opts) == False:
      print("inexlib_client.plotter.render : send_sg failed.")
      return False
    return True
