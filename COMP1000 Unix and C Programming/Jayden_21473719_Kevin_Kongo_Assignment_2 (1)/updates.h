#ifndef MAP_H
#define MAP_H
#include "terminal.h" /*Credit: Supplementary code provided by the lecturer*/
#include "components.h"
#include "linkedList.h"
void main_loop(int** map, playerPosition* player, carPosition* car, int num_row, int num_col, LinkedList* carHistory, LinkedList* playerHistory);
void update_player(playerPosition* player, char input, int num_row, int num_col);
void update_car(int** map, carPosition* car);

#endif