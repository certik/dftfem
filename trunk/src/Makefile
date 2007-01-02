all:
	cd solver-petsc && make
	cd mesh && make
	cd assembly && make

clean:
	cd solver-petsc && make distclean
	cd mesh && make clean
	cd assembly && make clean
	py.cleanup
