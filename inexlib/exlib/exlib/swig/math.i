// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

namespace inlib {

float fpi();
float ftwo_pi();
float fhalf_pi();

float fdeg2rad();
float frad2deg();

int fround(float a_x);

float fstep(float a_x);

float fcos(float x);
float fsin(float x);
float facos(float x);
float fasin(float x);
float ftan(float x);
float fatan(float x);
float fatan2(float x,float y);
float fsqrt(float x);
float fpow(float x,float y);
float fexp(float x);
float flog(float x);
float flog10(float x);
float ffloor(float x);
float fceil(float x);
float fcosh(float x);
float fsinh(float x);

float ffabs(float x);

float ffabsc(const float& x);

}

namespace inlib {

double pi();
double two_pi();
double half_pi();
double deg2rad();
double rad2deg();

}

//exlib_build_use skip
