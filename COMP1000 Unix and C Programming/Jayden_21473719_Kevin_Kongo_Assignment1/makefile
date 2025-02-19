CC = gcc
CFLAGS = -Wall -pedantic-errors -ansi -g
OBJ = main.o components.o updates.o newSleep.o terminal.o random.o
EXEC = traffic

$(EXEC) : $(OBJ)
	$(CC) $(OBJ) -o $(EXEC)

main.o : main.c components.h updates.h
	$(CC) -c main.c $(CFLAGS)

components.o : components.c components.h random.h
	$(CC) -c components.c $(CFLAGS)

updates.o : updates.c updates.h newSleep.h terminal.h components.h
	$(CC) -c updates.c $(CFLAGS)
	
newSleep.o : newSleep.c newSleep.h
	$(CC) -c newSleep.c $(CFLAGS)

terminal.o : terminal.c terminal.h
	$(CC) -c terminal.c $(CFLAGS)

random.o : random.c random.h
	$(CC) -c random.c $(CFLAGS)

clean : 
	rm -f $(EXEC) $(OBJ)