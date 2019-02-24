
import inlib
import base_plots
import exlib_offscreen as exlib

class plotter(base_plots.base_plots):
  m_gl2ps_mgr = None
  m_zb_mgr = None
  m_ttf = None
  m_sep = None
  m_plots = None
  m_width = 400
  m_height = 400
  
  def __del__(self):
    del self.m_zb_mgr
    del self.m_gl2ps_mgr
    del self.m_ttf
    del self.m_sep
    
  def __init__(self,a_out,a_cols,a_rows,a_width,a_height):
    inlib.env_append_path('EXLIB_FONT_PATH','./res')    
    inlib.env_append_path('EXLIB_FONT_PATH','../res')    

    #//////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////
    self.m_gl2ps_mgr = exlib.sg_gl2ps_manager()
    self.m_zb_mgr = inlib.sg_zb_manager()
    self.m_ttf = exlib.sg_text_freetype()

    #//////////////////////////////////////////////////////////
    #/// scene graph : ////////////////////////////////////////
    #//////////////////////////////////////////////////////////
    self.m_sep = inlib.sg_separator()
  
    camera = inlib.sg_ortho()
    camera.thisown = 0
    camera.height.value(1)
    z = 10*1
    camera.znear.value(0.1*z)
    camera.zfar.value(10*z)  # 100*z induces problems with lego rendering.
    camera.position.value(inlib.vec3f(0,0,z))
    camera.orientation.value(inlib.rotf(inlib.vec3f(0,0,1),0))
    camera.focal.value(z)
    self.m_sep.add(camera)
  
    #blend = inlib.sg_blend()
    #blend.thisown = 0
    #blend.on.value(True)
    #self.m_sep.add(blend)

    self.m_plots = inlib.sg_plots(self.m_ttf)
    self.m_plots.thisown = 0
    self.m_plots.set_regions(a_cols,a_rows)
    self.m_sep.add(self.m_plots)

    self.m_width = a_width
    self.m_height = a_height

    base_plots.base_plots.__init__(self,a_out,self.m_plots)
    
  def plot_histo(self,a_h):
    sgp = base_plots.base_plots.plot_histo(self,a_h)
    self.m_plots.adjust_size(self.m_width,self.m_height)
    return sgp    
  
  def plot_cloud2D(self,a_cloud):
    sgp = base_plots.base_plots.plot_cloud2D(self,a_cloud)
    self.m_plots.adjust_size(self.m_width,self.m_height)
    return sgp    

  def plot_cloud3D(self,a_cloud):    # spark_c3d_offscreen.py.
    sgp = base_plots.base_plots.plot_cloud3D(self,a_cloud)
    self.m_plots.adjust_size(self.m_width,self.m_height)
    return sgp    

  def plot(self,a_cloud):  # for rdirs_vis.py.
    self.plot_cloud3D(a_cloud)
    
  def out_ps(self,a_file = 'out.ps'):
    action = exlib.sg_gl2ps_action(self.m_gl2ps_mgr,inlib.get_cout(),self.m_width,self.m_height)
    action.open(a_file)
    self.m_sep.render(action)
    action.close()
    del action
      
  def out_zb_ps(self,a_file='out_zb.ps'):
    factor = 2  # have greater size to have good freetype rendering.
    _width = factor*self.m_width
    _height = factor*self.m_height
    action = inlib.sg_zb_action(self.m_zb_mgr,inlib.get_cout(),_width,_height)
    clear_color = inlib.colorf_white()
    action.zbuffer().clear_color_buffer(0)
    action.add_color(clear_color.r(),clear_color.g(),clear_color.b())
    action.zbuffer().clear_depth_buffer()
    self.m_sep.render(action)
    wps = inlib.wps(inlib.get_cout())
    if wps.open_file(a_file) == False :
      print("offscreen.plotter.render : inlib::sg::wps.open_file : failed.")
    else :      
      wps.PS_BEGIN_PAGE()
      wps.PS_PAGE_SCALE(_width,_height)
      wps.PS_IMAGE(action)
      wps.PS_END_PAGE()
      wps.close_file()
    
    del clear_color
    del wps
    del action
    
  def out_bsg(self,a_file='out.bsg'):
    action = inlib.sg_write_bsg(inlib.get_cout())
    if action.open_buffer() == False:
      print("offscreen.plotter.render : inlib::sg::write_bsg.open_buffer : failed.")
    elif self.m_sep.write(action) == False:
      print("offscreen.plotter.render : group.write() failed.")
    elif action.close_buffer() == False:
      print("offscreen.plotter.render : inlib::sg::write_bsg.close_buffer : failed.")
    elif action.write_file(a_file) == False:
      print("offscreen.plotter.render : inlib::sg::write_bsg.write_file : failed.")
    del action

  def write_paper(self,a_file,a_format):
    factor = 2  # have greater size to have good freetype rendering.
    _width = factor*self.m_width
    _height = factor*self.m_height
    clear_color = inlib.colorf_white()
    exlib.sg_write_paper(inlib.get_cout(),self.m_gl2ps_mgr,self.m_zb_mgr,\
                         clear_color.r(),clear_color.g(),clear_color.b(),clear_color.a(),\
                         self.m_sep,_width,_height,a_file,a_format)
    del clear_color
    
#format = 'GL2PS_EPS'
#format = "GL2PS_PS"
#format = "GL2PS_PDF"
#format = "GL2PS_SVG"
#format = "GL2PS_TEX"
#format = "GL2PS_PGF"
#format = "INZB_PS"
#format = "INZB_JPEG"
#format = "INZB_PNG"
