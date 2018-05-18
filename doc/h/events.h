/**

@page inexlib_py_events Events

<p>
  To have a default layout of the detector : 
@verbatim
     detector -> default
@endverbatim
 that leads to :
@image html detector_default.png
 Then click/touch on the bottom meta zone to return to the GUI and then
 the home button to have back the main menu.

  The application comes with a default data file (bdpi_ghost.dst)
 with two events. To view events you have first to open the data file
 with :
@verbatim
     home -> files -> dst -> bdpi_ghost.dst
@endverbatim
 When done, you can visualize an event with :
@verbatim
     home -> next event
@endverbatim

@image html event.png

 The home menu item "vis events" leads to a panel to loop on events.
 If looping on events, you can stop with "stop events". You can have
 a simple rotating animation of the scene with :
@verbatim
     home -> y rotate scene
@endverbatim
 (Touch/click again on this button to stop the animation).

@section inexlib_py_data_files More data files

  You can bring more data files and install them in the
 "document directory" of the inexlib_py application. The procedure
 is similar to what is explained in the ioda web pages
 under the "Data files" section (you have to replace
 "ioda" by "inexlib_py" in the explanations). You can use the "ftp"
 main menu item to get some files with the "good old FTP" from
 the inexlib_py download area but also from a site of your own by
 customizing a inexlib_py.ftp file deposited in the document
 directory (see the ioda Data files section for more).

*/

