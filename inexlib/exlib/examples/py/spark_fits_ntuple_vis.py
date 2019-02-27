# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

# To work on the cfitsio_write_ntuple.fits produced by exlib/examples/cpp/cfitsio_write_ntuple.cpp.
# The first hdu is a table containing three columns :
#   (int : row index, float : random gauss, double : random breit-wigner)

#///////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////

def project(row):
  if abs(row[1])<= 1: return row[1]
  if abs(row[2]-2)<= 0.5: return row[2]
  return None

#///////////////////////////////////////////////////////////////////////////////////////////////  
#/// main : ////////////////////////////////////////////////////////////////////////////////////  
#///////////////////////////////////////////////////////////////////////////////////////////////  
import pyspark.sql
import argparse

if __name__ == "__main__":
    
  #///////////////////////////////////////////////////////////////////////////////////////////////  
  #/// args : ////////////////////////////////////////////////////////////////////////////////////  
  #///////////////////////////////////////////////////////////////////////////////////////////////  
  parser = argparse.ArgumentParser()
  parser.add_argument('-verbose', dest='verbose',required=False,help='verbosity')
  parser.add_argument('-file', dest='file_name',required=True,help='Path to a data file')
  parser.add_argument('-hdu', dest='hdu',required=True,help='HDU index to load.')
  parser.add_argument('-vis_mode', dest='vis_mode',required=False,help='Visualization mode')
  parser.add_argument('-vis_host', dest='vis_host',required=False,help='host to display on')
  parser.add_argument('-vis_port', dest='vis_port',required=False,help='port to display on')
  parser.add_argument('-vis_format', dest='vis_format',required=False,help='format for output')
    
  args = parser.parse_args(None)

  #///////////////////////////////////////////////////////////////////////////////////////////////  
  #/// Spark : ///////////////////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////////////
  
  spark = pyspark.sql.SparkSession.builder.getOrCreate()

  # Set logs to be quiet :
  logger = spark.sparkContext._jvm.org.apache.log4j
  level = getattr(logger.Level, "OFF", "OFF")
  logger.LogManager.getLogger("org"). setLevel(level)
  logger.LogManager.getLogger("akka").setLevel(level)

  # Attach the data file to a DataFrame :
  df = spark.read.format("fits").option("hdu", args.hdu).load(args.file_name)
 #print("df.count() : "+str(df.count())+". Should be 10000.")
  df_count_ref = 10000
  if df.count() != df_count_ref :
    print("spark_fits_vis.py : df.count() "+str(df.count())+", expected "+str(df_count_ref))
    exit()

  data = df.collect()

  #///////////////////////////////////////////////////////////////////////////////////////////////  
  #/// plotting : ////////////////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////////////
  import inlib

  h_y = inlib.histo_h1d('y',100,-5,5)
  [h_y.fill(row[1],1) for row in data if row is not None]

  h_z = inlib.histo_h1d('z',100,-5,5)
  [h_z.fill(row[2],1) for row in data if row is not None]
  
 #data = df.repartition(256).rdd.map(lambda row: row[1]+row[2]).collect()
  data = df.rdd.map(lambda row: project(row)).collect()
 #print(data.__class__.__name__)       # list
 #print(data[0].__class__.__name__)    # float
  
  h_result = inlib.histo_h1d('z',100,-5,5)
  [h_result.fill(real,1) for real in data if real is not None]

  if args.vis_mode == "window" :
    #print("plot (window) ...")
    import window
    p = window.plotter(inlib.get_cout(),2,2,0,0,700,500)
    p.plot_histo(h_y)
    p.next()
    p.plot_histo(h_z)
    p.next()
    p.plot_histo(h_result)
    p.show()
    p.steer()
    del p
    
  elif args.vis_mode == "offscreen" :
    #print("plot (offscreen) ...")
    import offscreen
    p = offscreen.plotter(inlib.get_cout(),2,2,400,400)
    p.plot_histo(h_y)
    p.next()
    p.plot_histo(h_z)
    p.next()
    p.plot_histo(h_result)
    if args.vis_format == "bsg":
      p.out_bsg('out_spark_fits_ntuple_vis.bsg')
    else:      
      p.write_paper('out_spark_fits_ntuple_vis.ps','INZB_PS')
      p.write_paper('out_spark_fits_ntuple_vis.png','INZB_PNG')
    del p

  elif args.vis_mode == "client" :
    #print("plot (client) ...")

    import inexlib_client
    
    style_file = "./res/ioda.style"
    p = inexlib_client.plotter(inlib.get_cout(),2,2,args.vis_host,int(args.vis_port),style_file)
    p.plot_histo(h_y)
    p.next()
    p.plot_histo(h_z)
    p.next()
    p.plot_histo(h_result)

    #print("send plots ...")
  
    p.send_clear_static_scene()
    p.send_plots()
    del p

  else:
    #print("plot (gui_window) ...")
    import window
    p = window.gui_plotter(inlib.get_cout(),2,2,0,0,700,500)
    p.plot_histo(h_y)
    p.next()
    p.plot_histo(h_z)
    p.next()
    p.plot_histo(h_result)
    p.show()
    p.steer()
    del p
    
