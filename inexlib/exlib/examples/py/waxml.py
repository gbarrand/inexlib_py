# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

import inlib

EXIT_FAILURE = 1
EXIT_SUCCESS = 0

def main():
  writer = inlib.waxml_file()
  if writer.open('inlib_waxml.aida') == False :
    print("can't open inlib_axml.aida.")
    return EXIT_FAILURE

  entries = 1000000

  rg = inlib.rgaussd(1,2)

  h = inlib.histo_h1d('Gauss',100,-5,5)
  for count in range(0,entries) :
    h.fill(rg.shoot(),1.4)
  if writer.write(h,'/histo','rg') == False :
    print("can't write h1d.")
    return EXIT_FAILURE
  del rg,h,count

  rg = inlib.rgaussd(1,2)
  rbw = inlib.rbwd(0,1)
  h = inlib.histo_p1d('Profile',100,-5,5,-2,2)
  for count in range(0,entries) :
    h.fill(rg.shoot(),rbw.shoot(),1)
  if writer.write(h,'/histo','prof') == False :
    print("can't write prof.")
    return EXIT_FAILURE
  del rg,rbw,h,count

  rg = inlib.rgaussd(1,2)
  rbw = inlib.rbwd(0,1)
  h = inlib.histo_h2d('Gauss_BW',20,-5,5,20,-2,2)
  for count in range(0,entries) :
    h.fill(rg.shoot(),rbw.shoot(),0.8)
  if writer.write(h,'/histo','rgbw') == False :
    print("can't write h2d.")
    return EXIT_FAILURE
  del rg,rbw,h,count
  
  writer.close()
  del writer
  return EXIT_SUCCESS

main()
