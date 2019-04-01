// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

%rename(hep_polyhedron_tubs)  inlib::hep::polyhedron_tubs;

namespace inlib {
namespace hep {

class polyhedron {
public:
  polyhedron();
  virtual ~polyhedron(){}
public:
  polyhedron(const polyhedron&);
  polyhedron& operator=(const polyhedron&);
public:  
  polyhedron& Translate(double,double,double);
  polyhedron& Transform(const inlib::rotd& rot,double,double,double);
  polyhedron& Transform(const inlib::rotd& rot,const inlib::vec3d& trans);
  // Boolean operations 
  polyhedron add(const polyhedron &p) const;
  polyhedron subtract(const polyhedron &p) const;
  polyhedron intersect(const polyhedron &p) const;
};

class polyhedron_tubs : public polyhedron {
public:
  polyhedron_tubs(double Rmin, double Rmax, double Dz,double Phi1, double Dphi,int nstep = 0); //G.Barrand
  virtual ~polyhedron_tubs(){}
public:
  polyhedron_tubs(const polyhedron_tubs&);
  polyhedron_tubs& operator=(const polyhedron_tubs&);
};

class sf_polyhedron {
public:
  sf_polyhedron();
  virtual ~sf_polyhedron();
  sf_polyhedron(const sf_polyhedron&);
  sf_polyhedron& operator=(const sf_polyhedron&);
public:
  polyhedron& value();
  const polyhedron& value() const;
  void value(const polyhedron&);
};
 
}}

//exlib_build_use skip
