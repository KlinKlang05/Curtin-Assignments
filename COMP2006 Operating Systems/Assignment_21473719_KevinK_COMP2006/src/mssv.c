#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "fileio.h"
#include "threading.h"
#include "components.h"

int main(int argc, char* argv[]){
    int** mainboard = initialize_2d_int_array(BOARD_SIZE, BOARD_SIZE); // initialize board using dynamically allocated 2D array
    if (importSolution(argv[1], mainboard)){        // read file and copy to array
        printf("Issue importing file.\n\n");
        return 0;
    }

    pthread_mutex_t mutex_counter, mutex_total;
    pthread_mutex_init(&mutex_counter, NULL);   // mutex used for counting total valid rows, columns, sub-grids
    pthread_mutex_init(&mutex_total, NULL);     // mutex used for couting total number of validation attempts done. Used to find last thread to perform validation

    pthread_cond_t cond;
    pthread_cond_init(&cond, NULL);             // Condition variable used to block the parent thread

    int* row = (int*)calloc(9, sizeof(int));    // allocate shared arrays
    int* col = (int*)calloc(9, sizeof(int));
    int* sub = (int*)calloc(9, sizeof(int));
    int counter = 0, total = 0;                 // allocate counters

    Shared_Vars shared;                         // place all shared variables into a struct
    shared.board = mainboard;
    shared.col = col;
    shared.row = row; 
    shared.sub = sub;
    shared.counter = &counter;
    shared.mutex_c = &mutex_counter;
    shared.total = &total;
    shared.mutex_t = &mutex_total;
    shared.wake_cond = &cond;

    init_threads(shared, atoi(argv[2]));        // all threading logic is performed here
    
    if (counter == 27){
        printf("\nThere are 27 valid rows, columns, and sub-grids, thus the solution is valid.\n\n");
    }else{
        printf("\nThere are %d valid rows, columns, and sub-grids, thus the solution is invalid.\n\n", counter);
    }

    free(row);          // free allocated memory, mutex, and cond variables that were initialized
    free(col);
    free(sub);
    free_2d_int_array(mainboard, BOARD_SIZE);
    pthread_mutex_destroy(&mutex_counter);
    pthread_mutex_destroy(&mutex_total);
    pthread_cond_destroy(&cond);
    return 0;
}