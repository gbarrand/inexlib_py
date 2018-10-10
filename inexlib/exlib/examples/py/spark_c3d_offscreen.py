
from pyspark.sql import SparkSession

import numpy
import argparse

def plot_c3d(a_cloud):
  import exlib_offscreen as exlib

  gl2ps_mgr = exlib.sg_gl2ps_manager()
  zb_mgr = inlib.sg_zb_manager()

  #//////////////////////////////////////////////////////////
  #/// scene graph : ////////////////////////////////////////
  #//////////////////////////////////////////////////////////
  sep = inlib.sg_separator()
  sep.thisown = 0
  
  camera = inlib.sg_ortho()
  camera.thisown = 0
  camera.height.value(1)
  z = 10*1
  camera.znear.value(0.1*z)
  camera.zfar.value(10*z)  # 100*z induces problems with lego rendering.
  camera.position.value(inlib.vec3f(0,0,z))
  camera.orientation.value(inlib.rotf(inlib.vec3f(0,0,1),0))
  camera.focal.value(z)
  sep.add(camera)
  
  ttf = exlib.sg_text_freetype()
  
  plots = inlib.sg_plots(ttf)
  plots.thisown = 0
  plots.set_regions(1,1)
  sep.add(plots)
  
  #//////////////////////////////////////////////////////////
  #/// plot : ///////////////////////////////////////////////
  #//////////////////////////////////////////////////////////
  sgp = plots.current_plotter()

  sgp.shape.value(inlib.sg_plotter.xyz)
  sgp.shape_automated.value(False)
  
  sgp.points_style(0).color.value(inlib.colorf_red())
  sgp.points_style(0).marker_size.value(7)
  sgp.points_style(0).marker_style.value(inlib.marker_cross)

  sgp.infos_style().font.value(inlib.font_arialbd_ttf())
  sgp.infos_x_margin.value(0.01) #percent of plotter width.
  sgp.infos_y_margin.value(0.01) #percent of plotter height.
  
  sgp.plot(a_cloud)

  plots.view_border.value(False)

  width = 400
  height = 400

  plots.adjust_size(width,height)

  #//////////////////////////////////////////////////////////
  #/// output : /////////////////////////////////////////////
  #//////////////////////////////////////////////////////////

  waction = exlib.sg_gl2ps_action(gl2ps_mgr,inlib.get_cout(),width,height)
  waction.open('out.ps')
  sep.render(waction)
  waction.close()
  del waction
    
  #//////////////////////////////////////////////////////////
  #//////////////////////////////////////////////////////////
  factor = 2  # have greater size to have good freetype rendering.
  _width = factor*width
  _height = factor*height
  action = inlib.sg_zb_action(zb_mgr,inlib.get_cout(),_width,_height)
  clear_color = inlib.colorf_white()
  action.zbuffer().clear_color_buffer(0)
  action.add_color(clear_color.r(),clear_color.g(),clear_color.b())
  action.zbuffer().clear_depth_buffer()
  sep.render(action)
  wps = inlib.wps(inlib.get_cout())
  if wps.open_file("out_zb.ps") == False :
    print("inlib::sg::wps.open_file : failed")
    return
  wps.PS_BEGIN_PAGE()
  wps.PS_PAGE_SCALE(_width,_height)
  wps.PS_IMAGE(action)
  wps.PS_END_PAGE()
  wps.close_file()

  #//////////////////////////////////////////////////////////
  #//////////////////////////////////////////////////////////
  #//////////////////////////////////////////////////////////
  del zb_mgr
  del gl2ps_mgr
  
def mean(partition):
  xyz = [item for item in partition] # Unwrap the iterator
  size = len(xyz)

  # Compute the centroid only if the partition is not empty
  if size > 0:
    mean = numpy.mean(xyz, axis=0)
  else:
    mean = None

  yield (mean, size)

def quiet_logs(sc, log_level="ERROR"):
  # log_level : INFO, WARN, ERROR, OFF.
    
  logger = sc._jvm.org.apache.log4j
  level = getattr(logger.Level, log_level, "INFO")

  logger.LogManager.getLogger("org"). setLevel(level)
  logger.LogManager.getLogger("akka").setLevel(level)

if __name__ == "__main__":
    
  parser = argparse.ArgumentParser(description="Visualise the elements of a spatial RDD")
  parser.add_argument('-fits', dest='file_name',required=True,help='Path to a FITS file')
  parser.add_argument('-hdu', dest='hdu',required=True,help='HDU index to load.')
    
  args = parser.parse_args(None)

  # Initialize the Spark Session
  spark = SparkSession.builder.getOrCreate()

  # Set logs to be quiet
  quiet_logs(spark.sparkContext, log_level="OFF")

  # Load the data inside a DataFrame
  df = spark.read.format("fits").option("hdu", args.hdu).load(args.file_name)

  #data = df.repartition(256).rdd.collect()
  # Re-organise the data into lists of x, y, z coordinates
  #x = [p[0] for p in data if p is not None]
  #y = [p[1] for p in data if p is not None]
  #z = [p[2] for p in data if p is not None]

  # Apply a collapse function
  # Before, repartition our DataFrame to mimick a large data set.
  data = df.repartition(256).rdd.mapPartitions(lambda partition: mean(partition)).collect()
  # Re-organise the data into lists of x, y, z coordinates
  x = [p[0][0] for p in data if p[0] is not None]
  y = [p[0][1] for p in data if p[0] is not None]
  z = [p[0][2] for p in data if p[0] is not None]
  rad = numpy.array([p[1] for p in data if p[0] is not None])

  import inlib
  
  inlib.env_append_path('EXLIB_FONT_PATH','./res')    
  inlib.env_append_path('EXLIB_FONT_PATH','../res')    

 #inlib.spark_get_xyzs(x,y,z)
    
  #create and fill a 2D cloud :
  c3 = inlib.histo_c3d('xyz')
  for i in range(0,len(x)): c3.fill(x[i],y[i],z[i],1)

  print(c3.entries())
  print(c3.mean_y())
  print(c3.rms_y())
  print(c3.mean_z())
  print(c3.rms_z())

  plot_c3d(c3)
    
  print("end plotting.")
