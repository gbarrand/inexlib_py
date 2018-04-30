
build_dir=`pwd`
build_dir=`basename ${build_dir}`
#echo ${build_dir}

sep=':'
if [ "`uname | grep CYGWIN`" != "" ] ; then sep=';';fi

use_swig=yes  #no= use boost python

if [ ${use_swig} = yes ] ; then
  py_path="../../../exlib/spy"
  py_path="${py_path}${sep}.${sep}.."
else
  py_path=".${sep}.."
fi

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

ourex_home=../../../../../inexlib/ourex
ld_path="${ourex_home}/Python/${build_dir}"
if [ ${use_swig} = no ] ; then
ld_path="${ld_path}${sep}${ourex_home}/csz/${build_dir}"
ld_path="${ld_path}${sep}${ourex_home}/bpy/${build_dir}"
ld_path="${ld_path}${sep}${ourex_home}/glutess/${build_dir}"
ld_path="${ld_path}${sep}${ourex_home}/freetype/${build_dir}"
ld_path="${ld_path}${sep}${ourex_home}/gl2ps/${build_dir}"
fi
ld_curr=`printenv DYLD_LIBRARY_PATH`
if [ "${ld_curr}" = "" ] ; then
  DYLD_LIBRARY_PATH="${ld_path}"
  export DYLD_LIBRARY_PATH
else
  not_in=`echo "${ld_curr}" | grep "${ld_path}" `
  if [ "${not_in}" = "" ] ; then
    DYLD_LIBRARY_PATH="${DYLD_LIBRARY_PATH}${sep}${ld_path}"
    export DYLD_LIBRARY_PATH
  fi
fi
unset ld_curr
unset ld_path
