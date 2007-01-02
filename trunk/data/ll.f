      PARAMETER (NNVAL=5,NNGAU=16)
      COMMON /XCORP/ NVAL,NGAU,VA(5),VAL(3*NNGAU,NNVAL)



      READ(15,*,ERR=109) (VA(I),I=1,5)
      READ(15,*,ERR=109) NVAL,NGAU
	DO J=1,NVAL
	  READ(15,*,ERR=109) (VAL(I,J),I=1,3*NGAU)
	  WRITE(16,8572) (VAL(I,J),I=1,NGAU)
	  WRITE(16,8573) (VAL(I,J),I=NGAU+1,3*NGAU)
	  WRITE( *,8572) (VAL(I,J),I=1,NGAU)
	  WRITE( *,8573) (VAL(I,J),I=NGAU+1,3*NGAU)
	ENDDO
      ZN=VA(5)    ! naboj pseudo-jadra





C  HARTREE UNITS
	L1=L+1        ! L = 0,1,2,... (i.e. s,p,d, ...)
	DO 1 J=1,JQ   ! radial grid R(1)..R(JQ)
	  CORP=0.
	  DO 10 K=1,2
	    SQA=SQRT(VA(K))
	    X=SQA*R(J)
	    Q=ERFM(X)  ! error-function
   10	    CORP=CORP+VA(K+2)*Q
	  CORP=-CORP*VA(5)/R(J)
	  DO 11 K=1,NGAU
	    RJ=R(J)
	    Q=EXP(-RJ*RJ*VAL(K,L1))
	    Q=Q*(VAL(K+NGAU,L1)+RJ*RJ*VAL(K+2*NGAU,L1))
   11	    CORP=CORP+Q
    1	  U(J)=CORP   ! ionic pseudopotential
