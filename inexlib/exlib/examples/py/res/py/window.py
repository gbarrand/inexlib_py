
import inlib
import base_plots
import exlib_window as exlib

#////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
class plotter(base_plots.base_plots):
  m_gl2ps_mgr = None
  m_session = None
  m_plotter = None
  
  def __del__(self):
    del self.m_plotter
    del self.m_session
    del self.m_gl2ps_mgr
    
  def __init__(self,a_out,a_cols,a_rows,a_x,a_y,a_width,a_height):
    self.m_gl2ps_mgr = exlib.sg_gl2ps_manager()
    self.m_session = exlib.session(inlib.get_cout()) # screen manager
    if self.m_session.is_valid() == False :
      raise ValueError()
    self.m_plotter = exlib.plotter(self.m_session,a_cols,a_rows,a_x,a_y,a_width,a_height)
    if self.m_plotter.has_window() == False :
      raise ValueError()
    base_plots.base_plots.__init__(self,a_out,self.m_plotter.plots())
    
  def show(self):
    return self.m_plotter.show()
  def steer(self):
    return self.m_plotter.steer()
  def sync(self):
    return self.m_session.sync()
    
#////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
class gui_plotter(base_plots.base_plots):
  m_gl2ps_mgr = None
  m_session = None
  m_plotter = None
  
  def __del__(self):
    del self.m_plotter
    del self.m_session
    del self.m_gl2ps_mgr
    
  def __init__(self,a_out,a_cols,a_rows,a_x,a_y,a_width,a_height):
    self.m_gl2ps_mgr = exlib.sg_gl2ps_manager()
    self.m_session = exlib.session(inlib.get_cout()) # screen manager
    if self.m_session.is_valid() == False :
      raise ValueError()
    self.m_plotter = exlib.gui_plotter(self.m_session,a_cols,a_rows,a_x,a_y,a_width,a_height)
    if self.m_plotter.has_window() == False :
      raise ValueError()
    base_plots.base_plots.__init__(self,a_out,self.m_plotter.plots())
    
    self.m_plotter.set_plane_viewer(False)
    self.m_plotter.set_scene_light_on(False)
    self.m_plotter.hide_main_menu()
    self.m_plotter.hide_meta_zone()
    self.m_plotter.show_camera_menu()
      
  def show(self):
    return self.m_plotter.show()
  def steer(self):
    return self.m_plotter.steer()
  #def sync(self):
  #  return self.m_session.sync()
    
