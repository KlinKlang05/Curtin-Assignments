CC = gcc
CFLAGS = -Wall -pedantic -std=c99 -g
OBJ = mssv.o fileio.o threading.o components.o
EXEC = mssv

$(EXEC) : $(OBJ)
	$(CC) $(OBJ) -o $(EXEC)

mssv.o : mssv.c fileio.h threading.h components.h
	$(CC) -c mssv.c $(CFLAGS)

fileio.o : fileio.c fileio.h
	$(CC) -c fileio.c $(CFLAGS)

threading.o : threading.c threading.h components.h
	$(CC) -c threading.c $(CFLAGS)

components.o : components.c components.h
	$(CC) -c components.c $(CFLAGS)

clean : 
	rm -f $(EXEC) $(OBJ)