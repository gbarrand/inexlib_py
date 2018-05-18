# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

import os.path

file = '../../../data/pawdemo.root'
if os.path.isfile(file) == False :
  file = './pawdemo.root'
  if os.path.isfile(file) == False :
    print 'file pawdemo.root not found.'
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
    print "can't open file"
    return EXIT_FAILURE

  keys = rfile.dir().keys()
  #print 'number of keys = ',keys.size()

  dir = inlib.rroot_find_dir(rfile.dir(),'STAFF')
  if dir == None :
    print 'directory not found'
    return EXIT_FAILURE
    
  key = dir.find_key('h10')
  if key == None :
    print 'tree not found'
    return EXIT_FAILURE
    
  fac = inlib.rroot_fac(out)
  tree = inlib.rroot_key_to_tree(rfile,fac,key)
  if tree == None :
    print 'key is not a tree.'
    return EXIT_FAILURE

  #tree.show(gv.out(),1)
  #print tree.entries()
  
  leaf = tree.find_leaf("Age")
  if leaf == None :
    print 'leaf not found.'
    return EXIT_FAILURE

  #print 'leaf type : ',leaf.s_cls()

  li = inlib.rroot_cast_leaf_int(leaf)
  if leaf == None :
    print 'leaf not a leaf<int>.'
    return EXIT_FAILURE
  
  branch = tree.find_leaf_branch(leaf)
  if branch == None :
    print 'branch of leaf not found.'
    return EXIT_FAILURE


  h_age = inlib.histo_h1d('CERN/Age',100,0,100)

  for i in range(0,tree.entries()):
    if branch.find_entry(rfile,i) == False :
      print 'branch.find_entry failed.'
      return EXIT_FAILURE
    v = li.value(0)
    #print 'li ',i,' ',v
    h_age.fill(v,1)    

  rfile.close()

  print h_age.entries(),h_age.mean(),h_age.rms()
  
  #//////////////////////////////////////////////////
  #// plot : ////////////////////////////////////////
  #//////////////////////////////////////////////////

  import exlib

  gl2ps_mgr = exlib.sg_gl2ps_manager()
  smgr = exlib.session(inlib.get_cout()) # screen manager
  if smgr.is_valid() == True :
    plotter = exlib.plotter(smgr,1,1,0,0,700,500)
    if plotter.has_window() == True :
      sgp = plotter.plots().current_plotter()
      sgp.bins_style(0).color.value(inlib.colorf_blue())
 
      inlib.env_append_path('EXLIB_FONT_PATH','.')    
      inlib.env_append_path('EXLIB_FONT_PATH','..')    
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

      smgr.steer()

    del plotter

  del smgr
  #//////////////////////////////////////////////////
  #//////////////////////////////////////////////////
  #//////////////////////////////////////////////////


                
  
tree_main()
