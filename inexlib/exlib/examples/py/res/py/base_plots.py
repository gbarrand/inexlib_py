import inlib

#////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////
class base_plots:
  m_plots = None
  m_styles = None

  #def __del__(self):
    
  def __init__(self,a_out,a_plots):
    self.m_plots = a_plots
    self.m_plots.view_border.value(False)

    self.m_styles = inlib.xml_styles(a_out)

    self.m_styles.add_colormap("default",inlib.sg_style_default_colormap())
    self.m_styles.add_colormap("ROOT",inlib.sg_style_ROOT_colormap())

  def plots(self):
    return self.m_plots
    
  def next(self):
    self.m_plots.next()
    
  def plot_histo(self,a_h):
    sgp = self.m_plots.current_plotter()
    sgp.bins_style(0).color.value(inlib.colorf_blue())
    sgp.infos_style().font.value(inlib.font_arialbd_ttf())
    sgp.infos_x_margin.value(0.01) #percent of plotter width.
    sgp.infos_y_margin.value(0.01) #percent of plotter height.
    sgp.plot(a_h)
    return sgp
    
  def plot_histo_cp(self,a_h):
    sgp = self.m_plots.current_plotter()
    sgp.bins_style(0).color.value(inlib.colorf_blue())
    sgp.infos_style().font.value(inlib.font_arialbd_ttf())
    sgp.infos_x_margin.value(0.01) #percent of plotter width.
    sgp.infos_y_margin.value(0.01) #percent of plotter height.
    sgp.plot_cp(a_h)
    return sgp

  def plot_lego(self,a_h):
    sgp = self.m_plots.current_plotter()

    sgp.shape.value(inlib.sg_plotter.xyz)
    sgp.shape_automated.value(False)

    sgp.bins_style(0).color.value(inlib.colorf_blue())
    
    sgp.bins_style(0).modeling.value(inlib.modeling_boxes())
    sgp.bins_style(0).painting.value(inlib.painting_violet_to_red)

    sgp.infos_style().font.value(inlib.font_arialbd_ttf())
    sgp.infos_x_margin.value(0.01) #percent of plotter width.
    sgp.infos_y_margin.value(0.01) #percent of plotter height.
    sgp.plot(a_h)
    return sgp
    
  def plot_cloud2D(self,a_cloud):
    sgp = self.m_plots.current_plotter()

    sgp.points_style(0).color.value(inlib.colorf_blue())
   #sgp.points_style(0).modeling.value(inlib.modeling_markers())
   #sgp.points_style(0).marker_size.value(7)
   #sgp.points_style(0).marker_style.value(inlib.marker_dot)
   #sgp.points_style(0).marker_style.value(inlib.marker_cross)
    sgp.points_style(0).modeling.value(inlib.modeling_points())
   #sgp.points_style(0).point_size.value(10)

    sgp.infos_style().font.value(inlib.font_arialbd_ttf())
    sgp.infos_x_margin.value(0.01) #percent of plotter width.
    sgp.infos_y_margin.value(0.01) #percent of plotter height.
    sgp.plot(a_cloud)
    return sgp
    
  def plot_cloud3D(self,a_cloud):    # spark_c3d_offscreen.py.
    sgp = self.m_plots.current_plotter()

    sgp.shape.value(inlib.sg_plotter.xyz)
    sgp.shape_automated.value(False)
  
    sgp.points_style(0).color.value(inlib.colorf_blue())
   #sgp.points_style(0).modeling.value(inlib.modeling_markers())
   #sgp.points_style(0).marker_size.value(7)
   #sgp.points_style(0).marker_style.value(inlib.marker_dot)
   #sgp.points_style(0).marker_style.value(inlib.marker_cross)
    sgp.points_style(0).modeling.value(inlib.modeling_points())
    sgp.points_style(0).point_size.value(1)
  
    sgp.infos_style().font.value(inlib.font_arialbd_ttf())
    sgp.infos_x_margin.value(0.01) #percent of plotter width.
    sgp.infos_y_margin.value(0.01) #percent of plotter height.
    
    sgp.plot(a_cloud)
    return sgp

  def set_current_plotter_style(self,a_path):
    sgp = self.m_plots.current_plotter()
    inlib.sg_style_from_res(self.m_styles,a_path,sgp,False)
   
  def set_plotters_style(self,a_path):
    icurr = self.m_plots.current_index()
    plotn = self.m_plots.number()
    for index in range(0,plotn):
      if self.m_plots.set_current_plotter(index) == True:
        sgp = self.m_plots.current_plotter()
        inlib.sg_style_from_res(self.m_styles,a_path,sgp,False)
    self.m_plots.set_current_plotter(icurr)   
