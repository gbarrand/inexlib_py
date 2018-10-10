
from pyspark.sql import SparkSession

import argparse

def project(row):
  if abs(row[1])<= 1: return row[1]
  if abs(row[2]-2)<= 0.5: return row[2]
  return None

def plot_histo(a_h_y,a_h_z,a_h_r):
  import exlib_window as exlib
  gl2ps_mgr = exlib.sg_gl2ps_manager()
  smgr = exlib.session(inlib.get_cout()) # screen manager
  if smgr.is_valid() == True :
    plotter = exlib.plotter(smgr,2,2,0,0,700,700)
    if plotter.has_window() == True :

      sgp = plotter.plots().current_plotter()
      sgp.bins_style(0).color.value(inlib.colorf_blue())
      sgp.infos_style().font.value(inlib.font_arialbd_ttf())
      sgp.infos_x_margin.value(0.01) #percent of plotter width.
      sgp.infos_y_margin.value(0.01) #percent of plotter height.
      plotter.plot(a_h_y)

      plotter.plots().next()
      sgp = plotter.plots().current_plotter()
      sgp.bins_style(0).color.value(inlib.colorf_blue())
      sgp.infos_style().font.value(inlib.font_arialbd_ttf())
      sgp.infos_x_margin.value(0.01) #percent of plotter width.
      sgp.infos_y_margin.value(0.01) #percent of plotter height.
      plotter.plot(a_h_z)

      plotter.plots().next()
      sgp = plotter.plots().current_plotter()
      sgp.bins_style(0).color.value(inlib.colorf_blue())
      sgp.infos_style().font.value(inlib.font_arialbd_ttf())
      sgp.infos_x_margin.value(0.01) #percent of plotter width.
      sgp.infos_y_margin.value(0.01) #percent of plotter height.
      plotter.plot(a_h_r)

      plotter.plots().view_border.value(False)

      waction = exlib.sg_gl2ps_action(gl2ps_mgr,inlib.get_cout(),plotter.width(),plotter.height())
      waction.open('out.ps')
      plotter.sg().render(waction)
      waction.close()
      del waction
    
      plotter.show()

      plotter.steer()

    del plotter

  del smgr
  del gl2ps_mgr

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

  data = df.repartition(256).rdd.collect()

  x = [p[0] for p in data if p is not None]
  y = [p[1] for p in data if p is not None]
  z = [p[2] for p in data if p is not None]

  import inlib

  h_y = inlib.histo_h1d('y',100,-5,5)
  for i in range(0,len(y)): h_y.fill(y[i],1)

  h_z = inlib.histo_h1d('z',100,-5,5)
  for i in range(0,len(z)): h_z.fill(z[i],1)
  
  print(df.repartition(256).rdd.count())

 #result = df.repartition(256).rdd.map(lambda row: row[1]+row[2]).collect()
  result = df.repartition(256).rdd.map(lambda row: project(row)).collect()
 
  h_result = inlib.histo_h1d('z',100,-5,5)
  for i in range(0,len(result)):
    if result[i] != None: h_result.fill(result[i],1)
  
  plot_histo(h_y,h_z,h_result)

  print("end plotting.")
