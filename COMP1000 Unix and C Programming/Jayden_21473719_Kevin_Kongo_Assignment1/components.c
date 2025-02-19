#include <stdio.h>
#include <stdlib.h>
#include "components.h"
#define DEBUG

char** initialize_2d_char_array(int row_num, int col_num){
    char** arr;
    int c;
    arr = (char**)malloc(row_num * sizeof(char*));

    for(c = 0; c < row_num; c++){
        arr[c] = (char*)malloc(col_num * sizeof(char));
    }

    return arr;
}

int** initialize_2d_int_array(int row_num, int col_num){
    int** arr;
    int c;
    arr = (int**)malloc(row_num * sizeof(int*));

    for(c = 0; c < row_num; c++){
        arr[c] = (int*)malloc(col_num * sizeof(int));
    }

    return arr;
}

void free_2d_char_array(char** arr, int row_num){ 
    int c;
    for(c = 0; c < row_num; c++){
        free(arr[c]);
    }
    free(arr);
}

void free_2d_int_array(int** arr, int row_num){ /*need to discuss how to combine these two functions into one...*/
    int c;
    for(c = 0; c < row_num; c++){
        free(arr[c]);
    }
    free(arr);
} 

void refresh_map_array(char** map, int row_num, int col_num){
    int c;
    int d;

    for(c = 0; c < row_num; c++){
        for(d = 0; d < col_num; d++){
            if(d == col_num - 2){
                map[c][d] = '\n';
            }
            
            else if(d == col_num-1){
                map[c][d] = '\0';
            }
            
            else if(c == 0 || c == row_num - 1 || d == 0 || d == col_num - 3){
                map[c][d] = '*';
            }

            else if(c % 2 == 0){
                map[c][d] = '.';
            }
            
            else if(c == row_num-2 && d == col_num-4){
                map[c][d] = 'G';
            }
            else{
                map[c][d] = ' ';
            }
        }
    }
}

void initialize_cars(int** cars, char**map, int car_num, int row_num, int col_num){
    int col_pos;
    int direction;
    int i;
    char dir;
    initRandom();
    
    for(i=0; i<car_num; i++){ /*cars[i][0] = row position (will be fixed), cars[i][1] = col position (changes each frame), cars[i][2] = direction 1(right) 0(left)*/
        col_pos = randomUCP(1, col_num-4); 
        direction = randomUCP(0, 1);
        cars[i][0] = (i+1) * 2; /*Place on each row*/
        cars[i][1] = col_pos; /*Random Column position for each car*/
        cars[i][2] = direction; /*Random Direction*/
        
        if(col_pos == col_num - 4){ /*if car is on border, face it opposite direction...*/
            cars[i][2] = 0;
            dir = '<';
        }
        else if (col_pos == 1){
            cars[i][2] = 1;
            dir = '>';  
        }
        else if(direction == 0){ /*...Otherwise use random direction*/
            dir = '<';
        }
        else{
            dir = '>';
        }
        map[cars[i][0]][col_pos] = dir;
    }
}

