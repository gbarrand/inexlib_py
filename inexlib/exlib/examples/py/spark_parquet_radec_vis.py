# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

# To work on the (huge) xyz_v1.0.parquet file.

#///////////////////////////////////////////////////////////////////////////////////////
#/// main : ////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////

import pyspark.sql
import argparse

def fill_cut(a_c3,a_file,a_ra,a_dec,a_z):
  center_ra = 62
  half_ra = 0.9
  center_dec = -38.6
  half_dec = 0.9
  if center_ra-half_ra < a_ra and a_ra < center_ra+half_ra and\
     center_dec-half_dec < a_dec and a_dec < center_dec+half_dec:
    a_c3.fill(a_ra,a_dec,a_z,1)
    a_file.write(str(a_ra)+","+str(a_dec)+","+str(a_z)+"\n")
    
if __name__ == "__main__":
    
  #///////////////////////////////////////////////////////////////////////////////////////
  #/// args : ////////////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////
  parser = argparse.ArgumentParser()
  parser.add_argument('-verbose', dest='verbose',required=False,help='verbosity')
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
 
  df=df_all.select("ra","dec","redshift","halo_id")\
       .filter(df_all['redshift'].between(redshift_min,redshift_max))\
       .filter(df_all['halo_id']>0)\
       .drop('halo_id')

#       .sort("redshift", ascending=True)  # induces crash at exit : in python2.7/threading.py", line 801
#       .drop('halo_id','redshift')
#       .distinct()
    
  #print("df.count() : "+str(df.count()))

  #print("collect ...")
  data = df.collect()
  #print(data.__class__.__name__)       # list
  #print(data[0].__class__.__name__)    # Row
  #print(data[0][0].__class__.__name__) # float
  
  do_cut = True
  do_cut = False
  
  #///////////////////////////////////////////////////////////////////////////////////////
  #/// write csv : ///////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////
  import inlib
  
  #print("write csv ...")
  #file = open("out_radec_z.csv","w")
  #file.write("R,D,Z\n")
  #[file.write(str(row[0])+","+str(row[1])+","+str(row[2])+"\n") for row in data]
  #file.close()
  #exit
  
  #///////////////////////////////////////////////////////////////////////////////////////
  #/// plottting : ///////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////
  
  #print("fill c2d ...")
  #c2 = inlib.histo_c2d('radec')
  #[c2.fill(row[0],row[1],1) for row in data]

  #print("inlib::histo::c2d entries : "+str(c2.entries()))
  #print("  mean x = "+str(c2.mean_x())+", rms x = "+str(c2.rms_x()))
  #print("  mean y = "+str(c2.mean_y())+", rms y = "+str(c2.rms_y()))
  
  c3 = inlib.histo_c3d('radec_z')

  if do_cut == True:
    [fill_cut(c3,file,row[0],row[1],row[2]) for row in data]
  else:    
    [c3.fill(row[0],row[1],row[2],1) for row in data]

  
  #print("inlib::histo::c3d entries : "+str(c3.entries()))
  #print("  mean x = "+str(c3.mean_x())+", rms x = "+str(c3.rms_x()))
  #print("  mean y = "+str(c3.mean_y())+", rms y = "+str(c3.rms_y()))
  #print("  mean z = "+str(c3.mean_z())+", rms z = "+str(c3.rms_z()))
  
 #print("fill h2d ...")
 #h2 = inlib.histo_h2d('radec',100,0,360,100,-90,90)
 #h2 = inlib.histo_h2d('radec',200,c2.mean_x()-2*c2.rms_x(),c2.mean_x()+2*c2.rms_x(),\
 #                             200,c2.mean_y()-2*c2.rms_y(),c2.mean_y()+2*c2.rms_y())
 #[h2.fill(row[0],row[1],1) for row in data]
 #center_ra = 62
 #half_ra = 0.6
 #center_dec = -38.6
 #half_dec = 0.6
 #h2 = inlib.histo_h2d('radec',500,center_ra-half_ra,center_ra+half_ra,500,center_dec-half_dec,center_dec+half_dec)
 #[h2.fill(row[0],row[1],1) for row in data]
 #h2 = None

  if args.vis_mode == "window" :
    #print("plot (window) ...")
    import window
    p = window.plotter(inlib.get_cout(),1,1,0,0,700,500)
    p.plot_cloud3D(c3)
    #p.plot_cloud2D(c2)
    p.show()
    p.steer()
    del p
    
  elif args.vis_mode == "offscreen" :
    #print("plot (offscreen) ...")
    import offscreen
    p = offscreen.plotter(inlib.get_cout(),1,1,400,400)
    p.plot_cloud3D(c3)
    if args.vis_format == "bsg":
      p.out_bsg('out_spark_parquet_radec_vis.bsg')
    else:      
      p.write_paper('out_spark_parquet_radec_vis.ps','INZB_PS')
      p.write_paper('out_spark_parquet_radec_vis.png','INZB_PNG')
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
    
   #p.plot_cloud2D(c2)
   #p.next()
   #p.plot_lego(h2)
   #p.plot_histo(h2)

    #print("send plots ...")
  
    p.send_clear_static_scene()
    p.send_plots()
    del p

  else:
    #print("plot (gui_window) ...")
    import window
    p = window.gui_plotter(inlib.get_cout(),1,1,0,0,700,500)
    p.plot_cloud3D(c3)
    #p.plot_cloud2D(c2)
    p.show()
    p.steer()
    del p
    
  #del c2
  del c3
  #del h2

  print("end deleting. exit ...")
