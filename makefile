CC = clang
CFLAGS = -Wall -std=c99 -pedantic
PYTHON = /usr/lib/python3.7/config-3.7m-x86_64-linux-gnu

export LD_LIBRARY_PATH =`pwd`#

all:  _molecule.so 

clean:
	rm -f *.o *.so myprog

libmol.so: mol.o
	$(CC) $(CFLAGS) mol.o -shared -o libmol.so		

_molecule.so: molecule_wrap.o libmol.so
	$(CC) $(CLFAGS) molecule_wrap.o -shared  -L. -Wl,-rpath=. -lmol  -L $(PYTHON) -lpython3.7m -dynamiclib -o _molecule.so	

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -c molecule_wrap.c -fPIC -I /usr/include/python3.7m -o molecule_wrap.o

molecule_wrap.c molecule.py: molecule.i 
	swig -python molecule.i







	