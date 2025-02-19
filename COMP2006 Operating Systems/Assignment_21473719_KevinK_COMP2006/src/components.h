#ifndef COMPONENTS_H
#define COMPONENTS_H

int** initialize_2d_int_array(int row_num, int col_num);
void free_2d_int_array(int** arr, int row_num);
void atomic_increment(pthread_mutex_t* mutex, int* counter);
void atomic_increment_check_and_signal(pthread_mutex_t* mutex, pthread_cond_t* cond, int thread_num, int* shared_int);

#endif