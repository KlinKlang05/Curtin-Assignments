#ifndef THREADING_H
#define THREADING_H

#define BOARD_SIZE 9
#define NUM_THREADS 4
#define TOTAL_CHECKS 27 // defines the total amount of rows, columns, and subgrids that must be checked.



typedef struct shared{
    int* col;       // all of the shared data
    int* row;
    int* sub;  
    int** board;

    int* counter;
    pthread_mutex_t* mutex_c; // mutex for count
    int* total;
    pthread_mutex_t* mutex_t; // mutex for total checks that are done on sudoku board

    pthread_cond_t* wake_cond; // used for the last thread to wake the parent process
}Shared_Vars;

typedef struct args{    // arguments passed into the threads that handles sub-grids and rows
    int i_start;        // the index of the first row/subgrid number allocated to a thread (of 3)
    int thread_num;     // an ID number for the thread, it isn't the ID of type pthread_t
    int sleep_time;     // time that a thread will sleep for each column or row/subgrid it checks
    Shared_Vars shared; // all shared variables from the struct above are passed into here.
}Thread_Args;

void* validator_thread(void* _args);
void* col_validator_thread(void* _args);
void init_threads(Shared_Vars shared_variables, int sleep_time);

#endif