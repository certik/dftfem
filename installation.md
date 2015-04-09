## Download sources ##

```
svn checkout https://dftfem.googlecode.com/svn/trunk/ dftfem --username ondrej.certik
```

## Install contrib libraries ##

```
cd contrib
./make
```

This will install `arpack`, `petsc`, `slepc` and `libmesh` in the `contrib/lib` directory.

## Install dftfem ##

```
cd src
make
```