#ifndef COMPONENTS_H
#define COMPONENTS_Haw
#include "random.h"
char** initialize_2d_char_array(int row_num, int col_num);
int** initialize_2d_int_array(int row_num, int col_num);
void free_2d_char_array(char** arr, int row_num);
void free_2d_int_array(int** arr, int row_num);
void refresh_map_array(char** map, int row_num, int col_num);
void initialize_cars(int** cars, char**map, int car_num, int row_num, int col_num);


#endif