# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

#//////////////////////////////////////////////////////////
#/// args : ///////////////////////////////////////////////
#//////////////////////////////////////////////////////////
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-vis_host', dest='vis_host',required=True,help='host to display on')
parser.add_argument('-vis_port', dest='vis_port',required=True,help='port to display on')
args = parser.parse_args(None)

host = args.vis_host
port = int(args.vis_port)

#//////////////////////////////////////////////////////////
#/// inexlib client : /////////////////////////////////////
#//////////////////////////////////////////////////////////
import inlib

import exlib_offscreen as exlib

dc = exlib.net_sg_client(inlib.get_cout(),False,True)  #False=quiet, True=warn if receiving unknown protocol.

#print("try to connected to "+host+" "+str(port)+" ...")

if dc.initialize(host,port) == False:
  print("can't connect to "+host+" "+str(port))
  exit()

#print("connected to "+host+" "+str(port))

#//////////////////////////////////////////////////////////
#/// scene graph : ////////////////////////////////////////
#//////////////////////////////////////////////////////////
sep = inlib.sg_separator()
sep.thisown = 0

mtx = inlib.sg_matrix()  # for manip.
mtx.thisown = 0
sep.add(mtx)

mat = inlib.sg_rgba()
mat.thisown = 0
mat.color.value(inlib.colorf_green())
sep.add(mat)

node = inlib.sg_cube()
node.thisown = 0
sep.add(node)

#//////////////////////////////////////////////////////////
#/// send scene graph : ///////////////////////////////////
#//////////////////////////////////////////////////////////

if dc.send_string(inlib.sg_s_protocol_clear_static_sg()) == False:
  print("send protocol_s_rwc_clear_static_scene() failed.")
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

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
del sep
del dc
