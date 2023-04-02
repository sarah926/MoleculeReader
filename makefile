CC = clang
CFLAGS = -std=c99 -Wall -pedantic
HEADERPATH = /Library/Frameworks/Python.framework/Versions/3.11/include/python3.11
lib_path = /Library/Frameworks/Python.framework/Versions/3.11/lib/

all: _molecule.so # main

clean:
	rm -f *.o *.so
libmol.so: mol.o
	$(CC) mol.o -shared -o libmol.so
mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o
molecule_wrap.o: molecule_wrap.c molecule.py
	$(CC) $(CFLAGS) -c -fPIC -I $(HEADERPATH) molecule_wrap.c -o molecule_wrap.o

# molecule_wrap.o: molecule_wrap.c
# 	$(CC) $(CFLAGS) -c molecule_wrap.c -fPIC -I $(HEADERPATH) -o molecule_wrap.o

_molecule.so: libmol.so molecule_wrap.o molecule.py
	$(CC) -L$(lib_path) -lpython3.11  -L. -lmol -shared -dynamiclibrary -o _molecule.so molecule_wrap.o

#main: _molecule.so MolDisplay.py molecule.py
#python MolDisplay.py