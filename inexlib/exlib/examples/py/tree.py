# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

import os.path

#//////////////////////////////////////////////////////////
#/// args : ///////////////////////////////////////////////
#//////////////////////////////////////////////////////////
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-vis_mode', dest='vis_mode',required=False,help='Visualization mode')
parser.add_argument('-vis_host', dest='vis_host',required=False,help='host to display on')
parser.add_argument('-vis_port', dest='vis_port',required=False,help='port to display on')
parser.add_argument('-vis_format', dest='vis_format',required=False,help='format for output')
args = parser.parse_args(None)

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
file = '../../data/pawdemo.root'
if os.path.isfile(file) == False :
  file = '../data/pawdemo.root'
  if os.path.isfile(file) == False :
    file = './data/pawdemo.root'
    if os.path.isfile(file) == False :
      file = './pawdemo.root'
      if os.path.isfile(file) == False :
        print('file pawdemo.root not found.')
        exit()
    
import inlib

out = inlib.get_cout()

EXIT_FAILURE = 1
EXIT_SUCCESS = 0

#//////////////////////////////////////////////////
#// open the file and get an histo : //////////////
#//////////////////////////////////////////////////

def tree_main():
  rfile = inlib.rroot_file(inlib.get_cout(),file,False)
  if rfile.is_open() == False :
    print("can't open file")
    return EXIT_FAILURE

  keys = rfile.dir().keys()
  #print('number of keys = ');print(keys.size())

  dir = inlib.rroot_find_dir(rfile.dir(),'STAFF')
  if dir == None :
    print('directory not found')
    return EXIT_FAILURE
    
  key = dir.find_key('h10')
  if key == None :
    print('tree not found')
    return EXIT_FAILURE
    
  fac = inlib.rroot_fac(out)
  tree = inlib.rroot_key_to_tree(rfile,fac,key)
  if tree == None :
    print('key is not a tree.')
    return EXIT_FAILURE

  #tree.show(gv.out(),1)
  #print(tree.entries())
  
  leaf = tree.find_leaf("Age")
  if leaf == None :
    print('leaf not found.')
    return EXIT_FAILURE

  #print('leaf type : ');print(leaf.s_cls())

  li = inlib.rroot_cast_leaf_int(leaf)
  if leaf == None :
    print('leaf not a leaf<int>.')
    return EXIT_FAILURE
  
  branch = tree.find_leaf_branch(leaf)
  if branch == None :
    print('branch of leaf not found.')
    return EXIT_FAILURE


  h_age = inlib.histo_h1d('CERN/Age',100,0,100)

  for i in range(0,tree.entries()):
    if branch.find_entry(rfile,i) == False :
      print('branch.find_entry failed.')
      return EXIT_FAILURE
    v = li.value(0)
    h_age.fill(v,1)    

  rfile.close()

  print(h_age.entries())
  print(h_age.mean())
  print(h_age.rms())
  
  #//////////////////////////////////////////////////
  #// plot : ////////////////////////////////////////
  #//////////////////////////////////////////////////

  if args.vis_mode == "offscreen" :
    import offscreen
    p = offscreen.plotter(inlib.get_cout(),1,1,700,500)
    p.plot_histo(h_age)
    if args.vis_format == "bsg":
      p.out_bsg('out_tree.bsg')
    else:      
      p.write_paper('out_tree.ps','INZB_PS')
      p.write_paper('out_tree.png','INZB_PNG')
    del p

  elif args.vis_mode == "client" :
    import inexlib_client
    
    style_file = "./res/ioda.style"
    p = inexlib_client.plotter(inlib.get_cout(),1,1,args.vis_host,int(args.vis_port),style_file)
    p.plot_histo(h_age)

    #p.set_plotters_style("ROOT_default")
    if args.vis_host == "134.158.76.71":  #LAL/wallino.
      p.set_plotters_style("wall_ROOT_default")
    p.send_clear_static_scene()
    p.send_plots()
    del p

  else:
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
  
        plotter.plot(h_age)
  
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

  #//////////////////////////////////////////////////
  #//////////////////////////////////////////////////
  #//////////////////////////////////////////////////


                
  
tree_main()
