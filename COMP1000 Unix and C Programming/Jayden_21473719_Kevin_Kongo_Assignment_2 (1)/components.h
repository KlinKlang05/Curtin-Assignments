#ifndef COMPONENTS_H
#define COMPONENTS_H

typedef enum {UP, RIGHT, LEFT, DOWN} Direction;

typedef struct carPosition{
    int x; 
    int y;
    Direction dir; 
} carPosition;

typedef struct playerPosition{
    int x;
    int y;
    int goalx; /*x coordinate of the goal*/
    int goaly; /*y coordinate of the goal*/ /*These are stores in the player struct as they do not need to chang and are easy to access when checking the win condition.*/
} playerPosition;

char** initialize_2d_char_array(int row_num, int col_num); /*not used*/
int** initialize_2d_int_array(int row_num, int col_num);
void free_2d_char_array(char** arr, int row_num); /*not used*/
void free_2d_int_array(int** arr, int row_num);
void refresh_terminal(int** map, int row_num, int col_num, carPosition car, playerPosition player);
void initialize_positions(int** map, int row_num, int col_num, carPosition* car, playerPosition* player);
void freeStruct(void* structure);



#endif