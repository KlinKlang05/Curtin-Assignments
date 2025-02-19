CC = gcc
CFLAGS = -Wall -pedantic-errors -ansi -g
OBJ = main.o components.o updates.o terminal.o linkedList.o
EXEC = traffic

$(EXEC) : $(OBJ)
	$(CC) $(OBJ) -o $(EXEC)

main.o : main.c components.h updates.h
	$(CC) -c main.c $(CFLAGS)

components.o : components.c components.h linkedList.h
	$(CC) -c components.c $(CFLAGS)

updates.o : updates.c updates.h terminal.h components.h linkedList.h
	$(CC) -c updates.c $(CFLAGS)

terminal.o : terminal.c terminal.h
	$(CC) -c terminal.c $(CFLAGS)

linkedList.o : linkedList.c linkedList.h
	$(CC) -c linkedList.c $(CFLAGS)

clean : 
	rm -f $(EXEC) $(OBJ)