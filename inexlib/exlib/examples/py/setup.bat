@ECHO off 

REM # Usage :
REM #     DOS> call <osc_vis_path>\Python-setup.bat

IF DEFINED PYTHONPATH (
  SET PYTHONPATH=%PYTHONPATH%;..\..\..\exlib\spy;.;..
) ELSE (
  SET PYTHONPATH=..\..\..\exlib\spy;.;..
)

@ECHO on
