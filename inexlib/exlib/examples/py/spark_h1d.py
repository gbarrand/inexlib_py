
from pyspark.sql import SparkSession

import argparse

def plot_histo(a_h):
  import exlib_window as exlib
  gl2ps_mgr = exlib.sg_gl2ps_manager()
  smgr = exlib.session(inlib.get_cout()) # screen manager
  if smgr.is_valid() == True :
    plotter = exlib.plotter(smgr,1,1,0,0,700,500)
    if plotter.has_window() == True :
      sgp = plotter.plots().current_plotter()

      sgp.bins_style(0).color.value(inlib.colorf_blue())
      sgp.infos_style().font.value(inlib.font_arialbd_ttf())
      sgp.infos_x_margin.value(0.01) #percent of plotter width.
      sgp.infos_y_margin.value(0.01) #percent of plotter height.

      plotter.plot(a_h)

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

  # Apply a collapse function
  # Before, repartition our DataFrame to mimick a large data set.
  #data = df.repartition(256).rdd.mapPartitions(lambda partition: mean(partition)).collect()
  data = df.repartition(256).rdd.collect()

  # Re-organise the data into lists of x, y, z coordinates
  x = [p[0] for p in data if p is not None]
  y = [p[1] for p in data if p is not None]
  z = [p[2] for p in data if p is not None]

  import inlib

  h = inlib.histo_h1d('Rand gauss',100,-5,5)
  r = inlib.rgaussd(0,1)
  for i in range(0,10000): h.fill(r.shoot(),1)
  del r
  print(h.entries());print(h.mean());print(h.rms())
  plot_histo(h)

  print("end plotting.")
