
set build_dir=`pwd`
set build_dir=`basename ${build_dir}`
#echo ${build_dir}

set sep=':'
if ( "`uname | grep CYGWIN`" != "" ) then
  set sep=';'
endif

set use_swig=yes #no= use boost python

if ( "${use_swig}" == "yes" ) then
  set py_path="../../../exlib/spy"
  set py_path="${py_path}${sep}.${sep}.."
else
  set py_path=".${sep}.."
endif

set py_curr=`printenv PYTHONPATH`
if ( "${py_curr}" == "" ) then
  setenv PYTHONPATH "${py_path}"
else
  set not_in=`echo "${py_curr}" | grep "${py_path}" `
  if ( "${not_in}" == "" ) then
    setenv PYTHONPATH "${PYTHONPATH}${sep}${py_path}"
  endif
endif
unset py_curr
unset py_path

set ourex_home=../../../../../inexlib/ourex
set ld_path="${ourex_home}/Python/${build_dir}"
if ( "${use_swig}" == "no" ) then
set ld_path="${ld_path}${sep}${ourex_home}/csz/${build_dir}"
set ld_path="${ld_path}${sep}${ourex_home}/bpy/${build_dir}"
set ld_path="${ld_path}${sep}${ourex_home}/glutess/${build_dir}"
set ld_path="${ld_path}${sep}${ourex_home}/freetype/${build_dir}"
set ld_path="${ld_path}${sep}${ourex_home}/gl2ps/${build_dir}"
endif

set ld_curr=`printenv DYLD_LIBRARY_PATH`
if ( "${ld_curr}" == "" ) then
  setenv DYLD_LIBRARY_PATH "${ld_path}"
else
  set not_in=`echo "${ld_curr}" | grep "${ld_path}" `
  if ( "${not_in}" == "" ) then
    setenv DYLD_LIBRARY_PATH "${DYLD_LIBRARY_PATH}${sep}${ld_path}"
  endif
endif
unset ld_curr
unset ld_path

