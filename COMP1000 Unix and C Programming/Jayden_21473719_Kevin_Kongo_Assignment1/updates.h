#ifndef MAP_H
#define MAP_H
#include "newSleep.h" /*Credit: Supplementary code provided by the lecturer*/
#include "terminal.h" /*Credit: Supplementary code provided by the lecturer*/
#include "components.h"
void main_loop(char** map, int** car_array, int num_row, int num_col, int car_count);
void update_player(char** map, int* coords, int num_row, int num_col, char input);
void update_cars(char** map, int** car_array, int car_count, int num_row, int num_col);

#endif