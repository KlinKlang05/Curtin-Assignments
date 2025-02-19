#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>
#include <unistd.h>
#include <pthread.h>
#include "threading.h"
#include "components.h"



void* validator_thread(void* _args){
    Thread_Args* args = (Thread_Args*)_args;

    for (int i = args->i_start; i < args->i_start+3; i++){
        int row_dup = 0;
        int sub_dup = 0;

        int row_compare; // Used as temp variable to store each entry in a row/subgrid
        int sub_compare;

        for (int k = 0; k < BOARD_SIZE; k++){ 
            row_compare = (args->shared.board)[i][k];                                           
            sub_compare = (args->shared.board)[args->i_start + (int)floor(k/3)][(i%3)*3 + k%3]; 

            for (int j = 0; j < BOARD_SIZE; j++){    // search through each entry in a row/subgrid in nested loop, check if duplicates found
                if (row_compare == (args->shared.board)[i][j] && k != j){     
                    row_dup = 1;                                
                }
                if (sub_compare == (args->shared.board)[args->i_start + (int)floor(j/3)][(i%3)*3 + j%3] && k != j){
                    sub_dup = 1;
                }
            }
        }

        if (row_dup == 0){
            (args->shared.row)[i] = 1; // if row_sum is not zero, it is an invalid row
            atomic_increment(args->shared.mutex_c, args->shared.counter); // increment counter
        } 
        atomic_increment_check_and_signal(args->shared.mutex_t, args->shared.wake_cond,args->thread_num, args->shared.total); // increments total and wakes parent if this was the last validation
        sleep(args->sleep_time); // Sleep for given time as required in assignment specification
        
        if (sub_dup == 0){
            (args->shared.sub)[i] = 1; // if sub_sum is not zero, it is an invalid sub-grid
            atomic_increment(args->shared.mutex_c, args->shared.counter);  // increment counter
        }
        atomic_increment_check_and_signal(args->shared.mutex_t, args->shared.wake_cond,args->thread_num, args->shared.total); // increments total and wakes parent if this was the last validation
        sleep(args->sleep_time); // Sleep for given time as required in assignment specification
    }
    
    return NULL;
}

void* col_validator_thread(void* _args){
    Thread_Args* args = (Thread_Args*)_args;

    // printf("this is the column validator, thread id: %ld, thread num: %d\n", pthread_self(), args->thread_num);

    for (int i = 0; i < BOARD_SIZE; i++){
        int col_dup = 0;

        for (int k = 0; k < BOARD_SIZE; k++){   
            for (int j = 0; j < BOARD_SIZE; j++){   // search through each entry in a col in nested loop, check if duplicates found
                if ((args->shared.board)[k][i] == (args->shared.board)[j][i] && k != j){
                    col_dup = 1;
                }
            }
        }

        if (col_dup == 0){
            args->shared.col[i] = 1; // if col_sum is not zero, it is an invalid column
            atomic_increment(args->shared.mutex_c, args->shared.counter); // increment counter
        }
        atomic_increment_check_and_signal(args->shared.mutex_t, args->shared.wake_cond,args->thread_num, args->shared.total); // increments total and wakes parent if this was the last validation
        sleep(args->sleep_time); // Sleep for given time as required in assignment specification
    }

    return NULL;
}

void init_threads(Shared_Vars shared_variables, int sleep_time){
    
    pthread_t tid[NUM_THREADS];     // create an array of thread ID's
    
    Thread_Args validator_args[3];   // prepare arguments

    for (int i = 0; i < 3; i++){     // create the first three threads (for rows/subgrids) while passing correct arguments               
        validator_args[i].i_start = i*3;
        
        validator_args[i].shared = shared_variables;
        validator_args[i].thread_num = i+1;
        validator_args[i].sleep_time = sleep_time;
 
        pthread_create(&tid[i], NULL, validator_thread, &(validator_args[i]));
    }
    
    Thread_Args col_args;      // prepare arguments for column validator thread
    col_args.shared = shared_variables;
    col_args.thread_num = 4;
    col_args.sleep_time = sleep_time;

    pthread_create(&tid[3], NULL, col_validator_thread, &col_args);  // create the column validator thread

    pthread_mutex_lock(shared_variables.mutex_t);
    while (*(shared_variables.total) != TOTAL_CHECKS){  
        pthread_cond_wait(shared_variables.wake_cond, shared_variables.mutex_t); // wait for the last thread to wake the parent thread
    }
    pthread_mutex_unlock(shared_variables.mutex_t);

    for (int i = 0; i < 4; i++){              
        pthread_join(tid[i], NULL); // Join into threads to remove threads from memory
    }

    // print row and subgrid thread results
    for (int i = 0; i < 3; i++){
        printf("\nThread %d ID-%ld: ", i+1, tid[i+1]);
        int temp_state = 0;
        for (int k = i*3; k < i*3+3; k++){
            if (!(shared_variables.row[k])){
                printf("Row %d, ", k+1);
                temp_state = 1;
            }
            if (!(shared_variables.sub[k])){
                printf("Sub-Grid %d, ", k+1);
                temp_state = 1;
            }
        }
        if (temp_state){
            printf("is/are invalid\n");
        } else {
            printf("valid\n");
        }
    }

    // print col thread results
    printf("\nThread %d ID-%ld: ", 4, tid[4]);
    int temp_state = 0;
    for (int k = 0; k < BOARD_SIZE; k++){
        if (!(shared_variables.col[k])){
            printf("column %d, ", k+1);
            temp_state = 1;
        }
    }
    if (temp_state){
        printf("is/are invalid\n");
    } else {
        printf("valid\n");
    }
} 