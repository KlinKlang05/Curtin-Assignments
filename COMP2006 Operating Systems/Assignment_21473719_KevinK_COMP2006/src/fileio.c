#include <stdio.h>
#include "fileio.h"

int importSolution(char* filename, int** board){
    /*Get the solution data from the solution file and place into a 2D array. Return 0 if successful, else nonzero for error*/

    int i; int j;
    FILE* f = fopen(filename, "r");
    int filestate;

    if (f == NULL){
        perror("Could not open file");
        return 1;
    } else {
        for (i = 0; i < BOARD_SIZE; i++){
            for (j = 0; j < BOARD_SIZE; j++){
                filestate = fscanf(f, "%d ", board[i] + j);
            }
        }

        if (filestate == EOF){
            printf("File is not correct.\n\n\n");
            return 1;
        }
        
        fclose(f);
        return 0;
    }   
}