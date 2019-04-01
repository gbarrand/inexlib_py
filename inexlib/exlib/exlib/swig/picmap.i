// Copyright (C) 2010, Guy Barrand. All rights reserved.
// See the file exlib.license for terms.

%rename(SOPI_color) inlib::SOPI::color;
%rename(SOPI_cmap) inlib::SOPI::cmap;

%rename(SOPI_grey32) inlib::SOPI::grey32;
%rename(SOPI_greyinv32) inlib::SOPI::greyinv32;
%rename(SOPI_grey128) inlib::SOPI::grey128;
%rename(SOPI_greyinv128) inlib::SOPI::greyinv128;
%rename(SOPI_grey256) inlib::SOPI::grey256;
%rename(SOPI_col16) inlib::SOPI::col16;
%rename(SOPI_colrj32) inlib::SOPI::colrj32;
%rename(SOPI_colbr32) inlib::SOPI::colbr32;
%rename(SOPI_colrv32) inlib::SOPI::colrv32;
%rename(SOPI_colrj128) inlib::SOPI::colrj128;
%rename(SOPI_colbr128) inlib::SOPI::colbr128;
%rename(SOPI_red32) inlib::SOPI::red32;
%rename(SOPI_green32) inlib::SOPI::green32;
%rename(SOPI_blue32) inlib::SOPI::blue32;
%rename(SOPI_yellow32) inlib::SOPI::yellow32;
%rename(SOPI_orange32) inlib::SOPI::orange32;
%rename(SOPI_cyan32) inlib::SOPI::cyan32;
%rename(SOPI_violet32) inlib::SOPI::violet32;
%rename(SOPI_col64) inlib::SOPI::col64;
%rename(SOPI_rgb216) inlib::SOPI::rgb216;
%rename(SOPI_rgb512) inlib::SOPI::rgb512;
%rename(SOPI_rgb4096) inlib::SOPI::rgb4096;
%rename(SOPI_rgb32768) inlib::SOPI::rgb32768;
%rename(SOPI_midas_pastel) inlib::SOPI::midas_pastel;
%rename(SOPI_midas_heat) inlib::SOPI::midas_heat;
%rename(SOPI_midas_rainbow3) inlib::SOPI::midas_rainbow3;
%rename(SOPI_midas_bluered) inlib::SOPI::midas_bluered;
%rename(SOPI_midas_bluewhite) inlib::SOPI::midas_bluewhite;
%rename(SOPI_midas_stairs8) inlib::SOPI::midas_stairs8;
%rename(SOPI_midas_stairs9) inlib::SOPI::midas_stairs9;
%rename(SOPI_midas_staircase) inlib::SOPI::midas_staircase;
%rename(SOPI_midas_color) inlib::SOPI::midas_color;
%rename(SOPI_midas_manycol) inlib::SOPI::midas_manycol;
%rename(SOPI_midas_idl14) inlib::SOPI::midas_idl14;
%rename(SOPI_midas_idl15) inlib::SOPI::midas_idl15;

namespace inlib {
namespace SOPI {

class color {
public:
  color();
  color(inlib::ushort a_r,inlib::ushort a_g,inlib::ushort a_b);
  virtual ~color();
  color(const color&);
  color& operator=(const color&);
public:
  inlib::uchar rchar() const;
  inlib::uchar gchar() const;
  inlib::uchar bchar() const;
  float r() const;
  float g() const;
  float b() const;
};

class cmap {
public:
  static const color& black();
public:
  cmap(unsigned int);
  virtual ~cmap();
  cmap(const cmap&);
  cmap& operator=(const cmap&);
public:
  const color& get_color(unsigned int) const;
  size_t size() const;
};

class grey32 : public cmap {
public:
  grey32();
  virtual ~grey32();
  grey32(const grey32&);
  grey32& operator=(const grey32&);
};

class greyinv32 : public cmap {
public:
  greyinv32();
  virtual ~greyinv32();
  greyinv32(const greyinv32&);
  greyinv32& operator=(const greyinv32&);
};

class grey128 : public cmap {
public:
  grey128();
  virtual ~grey128();
  grey128(const grey128&);
  grey128& operator=(const grey128&);
};

class greyinv128 : public cmap {
public:
  greyinv128();
  virtual ~greyinv128();
  greyinv128(const greyinv128&);
  greyinv128& operator=(const greyinv128&);
};

class grey256 : public cmap {
public:
  grey256();
  virtual ~grey256();
  grey256(const grey256&);
  grey256& operator=(const grey256&);
};

class col16 : public cmap {
public:
  col16();
  virtual ~col16();
  col16(const col16&);
  col16& operator=(const col16&);
};

class colrj32 : public cmap {
public:
  colrj32();
  virtual ~colrj32();
  colrj32(const colrj32&);
  colrj32& operator=(const colrj32&);
};

class colbr32 : public cmap {
public:
  colbr32();
  virtual ~colbr32();
  colbr32(const colbr32&);
  colbr32& operator=(const colbr32&);
};

class colrv32 : public cmap {
public:
  colrv32();
  virtual ~colrv32();
  colrv32(const colrv32&);
  colrv32& operator=(const colrv32&);
};

class colrj128 : public cmap {
public:
  colrj128();
  virtual ~colrj128();
  colrj128(const colrj128&);
  colrj128& operator=(const colrj128&);
};

class colbr128 : public cmap {
public:
  colbr128();
  virtual ~colbr128();
  colbr128(const colbr128&);
  colbr128& operator=(const colbr128&);
};

class red32 : public cmap {
public:
  red32();
  virtual ~red32();
  red32(const red32&);
  red32& operator=(const red32&);
};

class green32 : public cmap {
public:
  green32();
  virtual ~green32();
  green32(const green32&);
  green32& operator=(const green32&);
};

class blue32 : public cmap {
public:
  blue32();
  virtual ~blue32();
  blue32(const blue32&);
  blue32& operator=(const blue32&);
};

class yellow32 : public cmap {
public:
  yellow32();
  virtual ~yellow32();
  yellow32(const yellow32&);
  yellow32& operator=(const yellow32&);
};

class orange32 : public cmap {
public:
  orange32();
  virtual ~orange32();
  orange32(const orange32&);
  orange32& operator=(const orange32&);
};

class cyan32 : public cmap {
public:
  cyan32();
  virtual ~cyan32();
  cyan32(const cyan32&);
  cyan32& operator=(const cyan32&);
};

class violet32 : public cmap {
public:
  violet32();
  virtual ~violet32();
  violet32(const violet32&);
  violet32& operator=(const violet32&);
};

class col64 : public cmap {
public:
  col64();
  virtual ~col64();
  col64(const col64&);
  col64& operator=(const col64&);
};

class rgb216 : public cmap {
public:
  rgb216();
  virtual ~rgb216();
  rgb216(const rgb216&);
  rgb216& operator=(const rgb216&);
};

class rgb512 : public cmap {
public:
  rgb512();
  virtual ~rgb512();
  rgb512(const rgb512&);
  rgb512& operator=(const rgb512&);
};

class rgb4096 : public cmap {
public:
  rgb4096();
  virtual ~rgb4096();
  rgb4096(const rgb4096&);
  rgb4096& operator=(const rgb4096&);
};

class rgb32768 : public cmap {
public:
  rgb32768();
  virtual ~rgb32768();
  rgb32768(const rgb32768&);
  rgb32768& operator=(const rgb32768&);
};

class midas_pastel : public cmap {
public:
  midas_pastel();
  virtual ~midas_pastel();
  midas_pastel(const midas_pastel&);
  midas_pastel& operator=(const midas_pastel&);
};

class midas_heat : public cmap {
public:
  midas_heat();
  virtual ~midas_heat();
  midas_heat(const midas_heat&);
  midas_heat& operator=(const midas_heat&);
};

class midas_rainbow3 : public cmap {
public:
  midas_rainbow3();
  virtual ~midas_rainbow3();
  midas_rainbow3(const midas_rainbow3&);
  midas_rainbow3& operator=(const midas_rainbow3&);
};

class midas_bluered : public cmap {
public:
  midas_bluered();
  virtual ~midas_bluered();
  midas_bluered(const midas_bluered&);
  midas_bluered& operator=(const midas_bluered&);
};

class midas_bluewhite : public cmap {
public:
  midas_bluewhite();
  virtual ~midas_bluewhite();
  midas_bluewhite(const midas_bluewhite&);
  midas_bluewhite& operator=(const midas_bluewhite&);
};

class midas_stairs8 : public cmap {
public:
  midas_stairs8();
  virtual ~midas_stairs8();
  midas_stairs8(const midas_stairs8&);
  midas_stairs8& operator=(const midas_stairs8&);
};

class midas_stairs9 : public cmap {
public:
  midas_stairs9();
  virtual ~midas_stairs9();
  midas_stairs9(const midas_stairs9&);
  midas_stairs9& operator=(const midas_stairs9&);
};

class midas_staircase : public cmap {
public:
  midas_staircase();
  virtual ~midas_staircase();
  midas_staircase(const midas_staircase&);
  midas_staircase& operator=(const midas_staircase&);
};

class midas_color : public cmap {
public:
  midas_color();
  virtual ~midas_color();
  midas_color(const midas_color&);
  midas_color& operator=(const midas_color&);
};

class midas_manycol : public cmap {
public:
  midas_manycol();
  virtual ~midas_manycol();
  midas_manycol(const midas_manycol&);
  midas_manycol& operator=(const midas_manycol&);
};

class midas_idl14 : public cmap {
public:
  midas_idl14();
  virtual ~midas_idl14();
  midas_idl14(const midas_idl14&);
  midas_idl14& operator=(const midas_idl14&);
};

class midas_idl15 : public cmap {
public:
  midas_idl15();
  virtual ~midas_idl15();
  midas_idl15(const midas_idl15&);
  midas_idl15& operator=(const midas_idl15&);
};

}}

//exlib_build_use skip
