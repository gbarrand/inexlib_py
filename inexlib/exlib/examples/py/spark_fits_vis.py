# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

#///////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////
import numpy

def mean(partition):
  xyz = [item for item in partition]
  
  #print(xyz.__class__.__name__)       # list
  #print(xyz[0].__class__.__name__)    # Row
  #print(xyz[0][0].__class__.__name__) # float
    
  size = len(xyz)   # should be 19683/256 = 76.88 but found to be 77. 
  
  # Compute the centroid only if the partition is not empty
  if size > 0:
    mean = numpy.mean(xyz, axis=0)
    #print(len(mean))                  # should be 3.
    #print(mean.__class__.__name__)    # ndarray
    #print(mean[0].__class__.__name__) # float64
  else:
    mean = None

  yield (mean, size)

#///////////////////////////////////////////////////////////////////////////////////////
#/// main : ////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////
import pyspark.sql
import argparse

if __name__ == "__main__":
    
  #///////////////////////////////////////////////////////////////////////////////////////
  #/// args : ////////////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////
  parser = argparse.ArgumentParser()
  parser.add_argument('-file', dest='file_name',required=True,help='Path to a data file')
  parser.add_argument('-hdu', dest='hdu',required=True,help='HDU index to load.')
  parser.add_argument('-vis_mode', dest='vis_mode',required=False,help='Visualization mode')
  parser.add_argument('-vis_host', dest='vis_host',required=False,help='host to display on')
  parser.add_argument('-vis_port', dest='vis_port',required=False,help='port to display on')
  parser.add_argument('-vis_format', dest='vis_format',required=False,help='format for output')
    
  args = parser.parse_args(None)

  #///////////////////////////////////////////////////////////////////////////////////////
  #/// Spark : ///////////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////
  # Initialize the Spark Session :
  spark = pyspark.sql.SparkSession.builder.getOrCreate()

  # Set logs to be quiet :
  logger = spark._jvm.org.apache.log4j
  log_level = "OFF"                                   # INFO, WARN, ERROR, OFF.
  level = getattr(logger.Level, log_level, "INFO")    # level__class__ is 'py4j.java_gateway.JavaObject'
  logger.LogManager.getLogger("org"). setLevel(level)
  logger.LogManager.getLogger("akka").setLevel(level)

  # Attach the data file to a DataFrame :
  df = spark.read.format("fits").option("hdu", args.hdu).load(args.file_name)
 #print("df.count() : "+str(df.count())+". Should be 19683.")
  df_count_ref = 19683
  if df.count() != df_count_ref :
    print("spark_fits_vis.py : df.count() "+str(df.count())+", expected "+str(df_count_ref))
    exit()
  
  # Do some manipulations on the data (scattered on nodes) and gather (last .collect()) result into the driver :
  data = df.repartition(256).rdd.mapPartitions(lambda partition: mean(partition)).collect()
 #print(data.__class__.__name__)          # list
 #print(data[0].__class__.__name__)       # ntuple
 #print(data[0][0].__class__.__name__)    # ndarray
 #print(data[0][0][0].__class__.__name__) # float64

  len_data = len(data)
  len_data_ref = 256
  if len_data != len_data_ref :
    print("spark_fits_vis.py : len(data)  "+str(len_data)+", expected "+str(len_data_ref))
    exit()
    
  ntuple = data[0]
  
 #print("len(ntuple) : "+str(len(ntuple))+". Should be 2.")
 #print(ntuple[0].__class__.__name__)          # ndarray
 #print(ntuple[1].__class__.__name__)          # int
 #print("data[0][1] : "+str(ntuple[1])+". Should be 77.")
  
  #///////////////////////////////////////////////////////////////////////////////////////
  #/// plotting : /////////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////
  import inlib

  c3 = inlib.histo_c3d('xyz')
  [c3.fill(ntuple[0][0],ntuple[0][1],ntuple[0][2],1) for ntuple in data if ntuple[0] is not None]
    
 #print("inlib::histo::c3d entries : "+str(c3.entries()))
 #print("  mean x = "+str(c3.mean_x())+", rms x = "+str(c3.rms_x()))
 #print("  mean y = "+str(c3.mean_y())+", rms y = "+str(c3.rms_y()))
 #print("  mean z = "+str(c3.mean_z())+", rms z = "+str(c3.rms_z()))
  
  if args.vis_mode == "window" :
    #print("plot (window) ...")
    import window
    p = window.plotter(inlib.get_cout(),1,1,0,0,700,500)
    p.plot_cloud3D(c3)
    p.show()
    p.steer()
    del p
    
  elif args.vis_mode == "offscreen" :
    #print("plot (offscreen) ...")
    import offscreen
    p = offscreen.plotter(inlib.get_cout(),1,1,400,400)
    p.plot_cloud3D(c3)
    if args.vis_format == "bsg":
      p.out_bsg('out_spark_fits_vis.bsg')
    else:      
      p.write_paper('out_spark_fits_vis.ps','INZB_PS')
      p.write_paper('out_spark_fits_vis.png','INZB_PNG')
    del p

  elif args.vis_mode == "client" :
    #print("plot inlib.c3d (client) ...")

    import inexlib_client
    
    style_file = "./res/ioda.style"
    p = inexlib_client.plotter(inlib.get_cout(),1,1,args.vis_host,int(args.vis_port),style_file)
    p.plot_cloud3D(c3)

    #print("send plots ...")
  
    p.send_clear_static_scene()
    p.send_plots()
    del p

  else:
    #print("plot (gui_window) ...")
    import window
    p = window.gui_plotter(inlib.get_cout(),1,1,0,0,700,500)
    p.plot_cloud3D(c3)
    p.show()
    p.steer()
    del p
    
