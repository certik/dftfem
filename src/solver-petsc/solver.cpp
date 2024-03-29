#include <fstream> 

static char help[] = "Solves a generalized eigensystem Ax=kBx with matrices loaded from a file.\n\n"
  "This example works for both real and complex numbers.\n\n"
  "The command line options are:\n\n"
  "  -f1 <filename>, where <filename> = matrix (A) file in PETSc binary form.\n"
  "  -f2 <filename>, where <filename> = matrix (B) file in PETSc binary form.\n\n";

#include "slepceps.h"

#if defined(PETSC_USE_COMPLEX)
    //it's probably going to work in REALs only
    stop()
#endif

PetscErrorCode ierr;
#define E(x) {ierr = x;CHKERRQ(ierr)}
#define print(x) E( PetscPrintf(PETSC_COMM_WORLD,x"\n") )

#undef __FUNCT__
#define __FUNCT__ "load"
int load(Mat *A, Mat *B)
{
  char        	 filename[256];
  PetscViewer 	 viewer;
  PetscTruth  	 flg;

  E( PetscOptionsGetString(PETSC_NULL,"-f1",filename,256,&flg) );
  if (!flg) {
    SETERRQ(1,"Must indicate a file name for matrix A with the -f1 option.");
  }

  E( PetscPrintf(PETSC_COMM_WORLD," Reading matrices from binary files...\n") );
  E( PetscViewerBinaryOpen(PETSC_COMM_WORLD,filename,FILE_MODE_READ,&viewer) );
  E( MatLoad(viewer,MATAIJ,A) );
  E( PetscViewerDestroy(viewer) );

  E( PetscOptionsGetString(PETSC_NULL,"-f2",filename,256,&flg) );
  if (!flg) {
    SETERRQ(1,"Must indicate a file name for matrix B with the -f2 option.");
  }

  E( PetscViewerBinaryOpen(PETSC_COMM_WORLD,filename,FILE_MODE_READ,&viewer) );
  E( MatLoad(viewer,MATAIJ,B) );
  E( PetscViewerDestroy(viewer) );
  return 0;
}

#undef __FUNCT__
#define __FUNCT__ "showinfo"
int showinfo(EPS eps)
{
  int         	 nev, maxit, its, lits;
  EPSType     	 type;
  PetscReal   	 tol;

  print(" -----------------------------------------------------------------");
  E( EPSGetIterationNumber(eps, &its) );
  E( PetscPrintf(PETSC_COMM_WORLD," Number of iterations of the method: %d\n",its) );
  //E( EPSGetNumberLinearIterations(eps, &lits) );
  E( PetscPrintf(PETSC_COMM_WORLD," Number of linear iterations of the method: %d\n",lits) );
  E( EPSGetType(eps,&type) );
  E( PetscPrintf(PETSC_COMM_WORLD," Solution method: %s\n\n",type) );
  E( EPSGetDimensions(eps,&nev,PETSC_NULL) );
  E( PetscPrintf(PETSC_COMM_WORLD," Number of requested eigenvalues: %d\n",nev) );
  E( EPSGetTolerances(eps,&tol,&maxit) );
  E( PetscPrintf(PETSC_COMM_WORLD," Stopping condition: tol=%.4g, maxit=%d\n",tol,maxit) );
  print(" -----------------------------------------------------------------");
  return 0;
}

void save_vec(Vec a, int k)
{
    if (k>0) return;
    PetscInt n;
    VecGetSize(a,&n);
    PetscScalar *y=new PetscScalar[n];
    PetscInt *ind=new PetscInt[n];
    for (int i=0;i<n;i++)
        ind[i]=i;
    VecGetValues(a,n,ind,y);
    std::ofstream f("../../tmp/sol.dat");
    for (int i=0;i<n;i++)
        f << y[i] << " ";
}


#undef __FUNCT__
#define __FUNCT__ "showsolutions"
int showsolutions(EPS eps, int size)
{
  PetscReal   	 error, re, im;
  PetscScalar 	 kr, ki;
  int         	 i, nconv;
  Vec   sol;
  E( VecCreate(PETSC_COMM_WORLD,&sol) );
  E( VecSetSizes(sol,PETSC_DECIDE,size) );
  E( VecSetType(sol,VECSEQ) );

  E( EPSGetConverged(eps,&nconv) );
  E( PetscPrintf(PETSC_COMM_WORLD," Number of converged approximate eigenpairs: %d\n\n",nconv) );
  if (nconv==0) return 0;

  E( PetscPrintf(PETSC_COMM_WORLD,
         "           k             ||Ax-kBx||/||kx||\n"
         "  --------------------- ------------------\n" ) );
  for( i=0; i<nconv; i++ ) 
  {
    E( EPSGetEigenpair(eps,i,&kr,&ki,sol,PETSC_NULL) );
    re = kr; im = ki;
    if (im == 0.0) 
        E( PetscPrintf(PETSC_COMM_WORLD,"       % 6f      ",re) )
    else 
        E( PetscPrintf(PETSC_COMM_WORLD," % 6f %+6f i",re,im) );
    E( EPSComputeRelativeError(eps,i,&error) );
    E( PetscPrintf(PETSC_COMM_WORLD," % 12f\n",error) );

    save_vec(sol,i);
  }
  print();
  return 0;
}

#undef __FUNCT__
#define __FUNCT__ "finalize"
int finalize(EPS eps, Mat A, Mat B)
{
  E( EPSDestroy(eps) );
  E( MatDestroy(A) );
  E( MatDestroy(B) );
  E( SlepcFinalize() );
  return 0;
}

#undef __FUNCT__
#define __FUNCT__ "setoptions"
int setoptions(EPS eps)
{
  E( EPSSetProblemType(eps,EPS_GNHEP) );

  ST st;
  E( EPSGetST(eps, &st) );
  E( STSetType(st,STSINV) );

  E( EPSSetFromOptions(eps) );
  return 0;
}

int get_size(Mat A)
{
    PetscInt m,n;
    E( MatGetSize(A,&m, &n) );
    return m;
}

#undef __FUNCT__
#define __FUNCT__ "main"
int main( int argc, char **argv )
{
  Mat A,B;		 
  EPS eps;		

  SlepcInitialize(&argc,&argv,(char*)0,help);
  print("\nGeneralized eigenproblem stored in file.\n");
  load(&A,&B);
  E( EPSCreate(PETSC_COMM_WORLD,&eps) );
  E( EPSSetOperators(eps,A,B) );
  setoptions(eps);

  print(" Solving...");
  E( EPSSolve(eps) );
  print("   done.");

  showinfo(eps);
  showsolutions(eps,get_size(A));
  finalize(eps,A,B);

  return 0;
}
