# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

# To work on xyz_v1.1.4_mass_and_mag_onepix.parquet

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
  #print("df_all.count() : "+str(df_all.count()))  # should be 17248794
  #print(df_all.columns)
  # column names should be :
  #   position_x position_y position_z
  #   velocity_x velocity_y velocity_z
  #   ra dec
  #   mag_g mag_u mag_i
  #   redshift
  #   halo_id
  #   is_central
  #
  #   spheroidMassStellar
  #   totalMassStellar
  #   hostHaloMass
  #   halo_mass
  #   baseDC2/target_halo_mass
  #   stellar_mass
  #   diskMassStellar
  #   stellar_mass_bulge
  #   stellar_mass_disk
  #   blackHoleMass

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

  df=df_all.select("position_x","position_y","position_z",\
                   "redshift",\
                   "mag_g","mag_u","mag_i",\
                   "halo_id")\
       .filter(df_all['redshift'].between(redshift_min,redshift_max))\
       .filter(df_all['halo_id']>0)\
       .drop('halo_id')

#       .sort("redshift", ascending=True)  # induces crash at exit : in python2.7/threading.py", line 801
#       .drop('halo_id','redshift')
#       .distinct()
    
  #print("df.count() : "+str(df.count()))

  data = df.collect()
  
  #///////////////////////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////
  import inlib
  
  #///////////////////////////////////
  #/// header sg : ///////////////////
  #///////////////////////////////////
  all_sep = inlib.sg_separator()
  #all_sep.thisown = 0
    
  camera = inlib.sg_ortho()
  camera.thisown = 0
  camera.position.value(inlib.vec3f(0,0,5))
  camera.height.value(2)
  camera.znear.value(0.1)
  camera.zfar.value(100)

  all_sep.add(camera)
  
  light = inlib.sg_head_light()
  light.thisown = 0
  light.direction.value(inlib.vec3f(1,-1,-10))
  #light.on.value(False)
  all_sep.add(light)
  
  #///////////////////////////////////
  #///////////////////////////////////
  #///////////////////////////////////
  
  sep = inlib.sg_separator()
  #sep.thisown = 0   # decided below.
  #all_sep.add(sep)  # decided below.

  #blend = inlib.sg_blend()
  #blend.thisown = 0
  #blend.on.value(True)
  #sep.add(blend)

  m = inlib.sg_matrix()
  m.thisown = 0
  sep.add(m)

  vtxs = inlib.sg_atb_vertices()
  vtxs.thisown = 0
  vtxs.mode.value(inlib.points())
  sep.add(vtxs)

  #cmap = inlib.SOPI_midas_idl14()
  cmap = inlib.SOPI_midas_heat()
  cmap_size = cmap.size()

  redshift_delta = redshift_max-redshift_min

  # mag_u : ultraviolet
  # mag_g : green
  # mag_r : red
  # mag_i : near infrared
  # mag_z : infrared

  i_pos_x = 0
  i_pos_y = 1
  i_pos_z = 2
  i_redshift = 3
  i_mag_g = 4
  i_mag_u = 5
  i_mag_i = 6

  mag_g_min = data[0][i_mag_g]
  mag_g_max = mag_g_min
  mag_u_min = data[0][i_mag_u]
  mag_u_max = mag_u_min
  mag_i_min = data[0][i_mag_i]
  mag_i_max = mag_i_min
  
  for row in data:
    mag_g = float(row[i_mag_g])
    if mag_g < mag_g_min : mag_g_min = mag_g
    if mag_g > mag_g_max : mag_g_max = mag_g
    mag_u = float(row[i_mag_u])
    if mag_u < mag_u_min : mag_u_min = mag_u
    if mag_u > mag_u_max : mag_u_max = mag_u
    mag_i = float(row[i_mag_i])
    if mag_i < mag_i_min : mag_i_min = mag_i
    if mag_i > mag_i_max : mag_i_max = mag_i
  mag_g_delta = mag_g_max-mag_g_min
  mag_u_delta = mag_u_max-mag_u_min
  mag_i_delta = mag_i_max-mag_i_min
  print(mag_g_min)
  print(mag_g_max)
  print(mag_u_min)
  print(mag_u_max)
  print(mag_i_min)
  print(mag_i_max)
    
  for row in data:
    mag_g = float(row[i_mag_g])
    mag_g_factor = (mag_g-mag_g_min)/mag_g_delta
    mag_u = float(row[i_mag_u])
    mag_u_factor = (mag_u-mag_u_min)/mag_u_delta
    mag_i = float(row[i_mag_i])
    mag_i_factor = (mag_i-mag_i_min)/mag_i_delta
    r = mag_i_factor
    g = mag_g_factor
    b = mag_u_factor
    r = 0;g = 0
    a = 1
    #icolor = int(color_factor*(cmap_size-1))
    #icolor = int((1.0-color_factor)*(cmap_size-1))
    #SOPI_color = cmap.get_color(icolor)  # with midas_heat : icolor 0 is black, size-1 is white.
    #r = SOPI_color.r()
    #g = SOPI_color.g()
    #b = SOPI_color.b()
    #a = 1
    vtxs.add_pos_color(float(row[i_pos_x]),float(row[i_pos_y]),float(row[i_pos_z]),r,g,b,a)
  
  vtxs.center()

  #///////////////////////////////////////////////////////////////////////////////////////
  #/// plottting : ///////////////////////////////////////////////////////////////////////
  #///////////////////////////////////////////////////////////////////////////////////////
  
  width = 700
  height = 500
  
  if args.vis_mode == "offscreen" :
    import exlib_offscreen as exlib
    sep.thisown = 0
    all_sep.add(sep)
    camera.height.value(400)
    gl2ps_mgr = exlib.sg_gl2ps_manager()
    zb_mgr = inlib.sg_zb_manager()
    factor = 2  # have greater size to have good freetype rendering.
    _width = factor*width
    _height = factor*height
    clear_color = inlib.colorf_white()
    file = 'out_spark_colored_galaxies.ps'
    format = "INZB_PS"
    exlib.sg_write_paper(inlib.get_cout(),gl2ps_mgr,zb_mgr,\
                         clear_color.r(),clear_color.g(),clear_color.b(),clear_color.a(),\
                         all_sep,_width,_height,file,format)
    file = 'out_spark_colored_galaxies.png'
    format = "INZB_PNG"
    exlib.sg_write_paper(inlib.get_cout(),gl2ps_mgr,zb_mgr,\
                         clear_color.r(),clear_color.g(),clear_color.b(),clear_color.a(),\
                         all_sep,_width,_height,file,format)
    del clear_color
    del zb_mgr
    del gl2ps_mgr
    del all_sep

  elif args.vis_mode == "client" :
    del all_sep

    host = args.vis_host
    port = int(args.vis_port)
    #print("try to connected to "+host+" "+str(port)+" ...")
  
    import exlib_offscreen as exlib
    dc = exlib.net_sg_client(inlib.get_cout(),False,True)  #False=quiet, True=warn if receiving unknown protocol.
    if dc.initialize(host,port) == False:
      print("can't connect to "+host+" "+str(port))
      exit()

    if dc.send_string(inlib.sg_s_protocol_clear_static_sg()) == False:
      print("send protocol_clear_static_scene() failed.")
      exit()

    opts = inlib.args()
    opts.add(inlib.sg_s_send_placement(),inlib.sg_s_placement_static())
    if dc.send_sg(sep,opts) == False:
      print("send_sg failed.")
      exit()

    if dc.socket().send_string(inlib.sg_s_protocol_disconnect()) == False:
      print("send protocol_s_disconnect() failed.")
      exit()

    dc.socket().disconnect()
    del dc

    del sep
    
  else:
    print('exit viewer steering by closing the window with the mouse.')
    import exlib_window as exlib
    smgr = exlib.session(inlib.get_cout()) # screen manager
    if smgr.is_valid() == True :
      viewer = exlib.gui_viewer_window(smgr,0,0,width,height)
      if viewer.has_window() == True :
        sep.thisown = 0
        all_sep.add(sep)
        all_sep.thisown = 0
        viewer.scene().add(all_sep);
        
        viewer.set_scene_camera(camera);
        viewer.set_scene_light(light);
  
        viewer.set_plane_viewer(False);
        viewer.set_scene_light_on(True);
    
        viewer.adapt_camera_to_scene()
        
        viewer.hide_main_menu();
        viewer.hide_meta_zone();
        viewer.show_camera_menu();
  
        viewer.scene_camera().da.value(0.0017)
        viewer.scene_camera().ds.value(0.999)

        #ortho = inlib.sg_cast_ortho(viewer.scene_camera())
        #print(ortho.height.value_cp())
    
        viewer.show();
        viewer.steer();

        print("end steer.")
      
      del viewer
    del smgr

  print("end deleting. exit ...")
