#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "components.h"
#include "threading.h"

int** initialize_2d_int_array(int row_num, int col_num){    // initialize dynamically allocated 2D array
    int** arr;
    int c;
    arr = (int**)malloc(row_num * sizeof(int*));

    for(c = 0; c < row_num; c++){
        arr[c] = (int*)calloc(col_num, sizeof(int));
    }

    return arr;
}

void free_2d_int_array(int** arr, int row_num){             // free dynamically alocated 2D array
    int c;
    for(c = 0; c < row_num; c++){
        free(arr[c]);
    }
    free(arr);
} 

void atomic_increment(pthread_mutex_t* mutex, int* counter){ // used to increment integers atomically to prevent race condition
    pthread_mutex_lock(mutex);
    *counter += 1;
    pthread_mutex_unlock(mutex);
}

void atomic_increment_check_and_signal(pthread_mutex_t* mutex, pthread_cond_t* cond, int thread_num, int* shared_int){  // Each thread must increment a counter every validation, then check if it's the last thread to complete a validation using that counter
    pthread_mutex_lock(mutex);
    *shared_int += 1;
    if (*shared_int == TOTAL_CHECKS){
        printf("Thread ID-%d is the last thread.\n", thread_num);
        pthread_cond_signal(cond); // Wake parent thread if all checks have completed
    }
    pthread_mutex_unlock(mutex);
}