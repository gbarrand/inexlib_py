# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

# to check that we can use inexlib_py within a .py executed within spark.

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
  parser.add_argument('-vis_mode', dest='vis_mode',required=False,help='Visualization mode')
  parser.add_argument('-vis_host', dest='vis_host',required=False,help='host to display on')
  parser.add_argument('-vis_port', dest='vis_port',required=False,help='port to display on')
  parser.add_argument('-vis_format', dest='vis_format',required=False,help='format for output')
    
  args = parser.parse_args(None)

  #///////////////////////////////////////////////////////////////////////////////////////////////  
  #/// Spark : ///////////////////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////////////
  spark = pyspark.sql.SparkSession.builder.getOrCreate()

  logger = spark._jvm.org.apache.log4j
  log_level = "OFF"                                   # INFO, WARN, ERROR, OFF.
  level = getattr(logger.Level, log_level, "INFO")    # level__class__ is 'py4j.java_gateway.JavaObject'
  logger.LogManager.getLogger("org"). setLevel(level)
  logger.LogManager.getLogger("akka").setLevel(level)

  #///////////////////////////////////////////////////////////////////////////////////////////////  
  #/// inlib and plotting : //////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////////////
  import inlib

  h = inlib.histo_h1d('Rand gauss',100,-5,5)
  r = inlib.rgaussd(0,1)
  for i in range(0,10000): h.fill(r.shoot(),1)
  del r

  entries = h.entries()
  entries_ref = 10000
  if entries != entries_ref :
    print("spark_inlib_h1d.py : entries "+str(entries)+", expected "+str(entries_ref))
    exit()

 #print(h.entries());print(h.mean());print(h.rms())
 
  if args.vis_mode == "window" :
    import window
    p = window.plotter(inlib.get_cout(),1,1,0,0,700,500)
    p.plot_histo(h)
    p.show()
    p.steer()
    del p

  elif args.vis_mode == "offscreen" :
    import offscreen
    p = offscreen.plotter(inlib.get_cout(),0,0,700,500)
    p.plot_histo(h)
    if args.vis_format == "bsg":
      p.out_bsg('out_spark_inlib_h1d_visbsg')
    else:      
      p.write_paper('out_spark_inlib_h1d_vis.ps','INZB_PS')
      p.write_paper('out_spark_inlib_h1d_vis.png','INZB_PNG')
    del p
    
  elif args.vis_mode == "client" :
    import inexlib_client
    style_file = "./res/ioda.style"
    p = inexlib_client.plotter(inlib.get_cout(),1,1,args.vis_host,int(args.vis_port),style_file)
    p.plot_histo(h)
    #print("send plots ...")
    p.send_clear_static_scene()
    p.send_plots()
    del p

  else:
    import window
    p = window.gui_plotter(inlib.get_cout(),1,1,0,0,700,500)
    p.plot_histo(h)
    p.show()
    p.steer()
    del p

