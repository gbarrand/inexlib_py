
# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

#/////////////////////////////////////////////////////////////////
#/// PYTHONPATH : ////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////

spy_dir=spy
if [ "`./bin/which_py`" = Python3 ] ; then spy_dir=spy3;fi    

sep=':'
if [ "`uname | grep CYGWIN`" != "" ] ; then sep=';' ;fi

py_path="./res/py"
py_path="${py_path}${sep}./res/${spy_dir}"
py_path="${py_path}${sep}./modules"

py_curr=`printenv PYTHONPATH`
if [ "${py_curr}" = "" ] ; then
  PYTHONPATH="${py_path}"
  export PYTHONPATH
else
  not_in=`echo "${py_curr}" | grep "${py_path}" `
  if [ "${not_in}" = "" ] ; then
    PYTHONPATH="${PYTHONPATH}${sep}${py_path}"
    export PYTHONPATH
  fi
fi
unset py_curr
unset py_path
unset sep
unset spy_dir

#echo 'PYTHONPATH :'
#printenv PYTHONPATH
