
# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

#/////////////////////////////////////////////////////////////////
#/// PYTHONPATH : ////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////

set spy_dir=spy
if ( "`./bin/which_py`" == "Python3" ) then
  set spy_dir=spy3
endif

set sep=':'
if ( "`uname | grep CYGWIN`" != "" ) then
  set sep=";"
endif

set py_path="./res/py"
set py_path="${py_path}${sep}./res/${spy_dir}"
set py_path="${py_path}${sep}./modules"

set py_curr=`printenv PYTHONPATH`
if ( "${py_curr}" == "" ) then
  setenv PYTHONPATH "${py_path}"
else
  if ( `echo "${py_curr}" | grep "${py_path}" ` == "" ) then
    setenv PYTHONPATH "${PYTHONPATH}${sep}${py_path}"
  endif
endif

unset py_curr
unset py_path
unset sep
unset spy_dir

#echo 'PYTHONPATH :'
#printenv PYTHONPATH
