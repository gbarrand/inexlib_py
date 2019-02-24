# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

# To work on the (huge) xyz_v1.0.parquet file.

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
  parser.add_argument('-vis_mode', dest='vis_mode',required=False,help='Visualization mode')
  parser.add_argument('-vis_host', dest='vis_host',required=False,help='host to display on')
  parser.add_argument('-vis_port', dest='vis_port',required=False,help='port to display on')
  parser.add_argument('-vis_format', dest='vis_format',required=False,help='format for output')
  parser.add_argument('-redshift_min', dest='redshift_min',required=False,help='redshift_min')
  parser.add_argument('-redshift_max', dest='redshift_max',required=False,help='redshift_max')

  args = parser.parse_args(None)
  
  #///////////////////////////////////////////////////////////////////////////////////////
  #/// Spark : ///////////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////
  spark = pyspark.sql.SparkSession.builder.getOrCreate()

  # Set logs to be quiet
  logger = spark._jvm.org.apache.log4j
  log_level = "OFF"
  level = getattr(logger.Level, log_level, "INFO")
  logger.LogManager.getLogger("org"). setLevel(level)
  logger.LogManager.getLogger("akka").setLevel(level)

  df_all = spark.read.parquet(args.file_name)
 #print("df_all.count() : "+str(df_all.count()))
 #print(df_all.columns)

  if args.redshift_min == None:
    redshift_min = 1  # Stephane cut.
  else:    
    redshift_min = float(args.redshift_min)
  
  if args.redshift_max == None:
   #redshift_max= 1.003
   #redshift_max = 1.02 # without halo_id cut, it is the lower value than does not crash.
    redshift_max = 1.2  # Stephane cut.
  else:    
    redshift_max = float(args.redshift_max)
  
 #print("redshift_min : "+str(redshift_min))
 #print("redshift_max : "+str(redshift_max))

  # Patricia Larsen :
  #redshift_min = 0.95
  #redshift_max = 1.0

  #print("avec distinct")
  #print("sans distinct")
  #print("sort position_z")
  
  df = df_all.select('position_x','position_y','position_z','redshift','halo_id')\
    .filter(df_all['redshift'].between(redshift_min,redshift_max))\
    .filter(df_all['halo_id']>0)\
    .drop('halo_id')

#    .sort("position_z", ascending=True)\
#    .sort("redshift", ascending=True)
#    .dropDuplicates()
#    .distinct()
#    .sample(False,0.1)
    
  #from pyspark.sql import functions as F
  #df=df_all.select("halo_id","ra","dec","redshift")\
  #     .filter(df_all['redshift'].between(redshift_min,redshift_max))\
  #     .filter(df_all['halo_id']>0)
  #df=df.withColumn("x",df.redshift*F.sin(F.radians(90-df.dec))*F.cos(F.radians(df.ra)))\
  #     .withColumn("y",df.redshift*F.sin(F.radians(90-df.dec))*F.sin(F.radians(df.ra)))\
  #     .withColumn("z",df.redshift*F.cos(F.radians(90-df.dec)))\
  #     .drop('ra','dec')

 #print("df.count() : "+str(df.count()))

 #print("collect ...")
  data = df.collect()
  #print(data.__class__.__name__)       # list
  #print(data[0].__class__.__name__)    # Row
  #print(data[0][0].__class__.__name__) # float
  
  #///////////////////////////////////////////////////////////////////////////////////////
  #/// plottting : ///////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////
  #print("write csv ...")
  #file = open("out_pos_xyz_z.csv","w")
  #file.write("position_x,position_y,position_z,redshift\n")
  #[file.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+"\n") for row in data]
  #file.close()
  #exit(0)

  #print("fill c3d ...")
  
  import inlib
  
  #create and fill a 2D cloud :
  c3 = inlib.histo_c3d('xyz')
  [c3.fill(row[0],row[1],row[2],1) for row in data]

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
      p.out_bsg('out_spark_parquet_vis.bsg')
    else:      
      p.write_paper('out_spark_parquet_vis.ps','INZB_PS')
      p.write_paper('out_spark_parquet_vis.png','INZB_PNG')
    del p

  elif args.vis_mode == "client" :
    #print("plot (client) ...")
    
    import inexlib_client

    style_file = "./res/ioda.style"
    p = inexlib_client.plotter(inlib.get_cout(),1,1,args.vis_host,int(args.vis_port),style_file)
    p.m_blend.on.value(True)
    sgp = p.plot_cloud3D(c3)
    blue = inlib.colorf_blue()
    blue.set_a(0.5)
    sgp.points_style(0).color.value(blue)
    sgp.theta.value(0)
    sgp.phi.value(0)
    sgp.tau.value(0)

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
    
