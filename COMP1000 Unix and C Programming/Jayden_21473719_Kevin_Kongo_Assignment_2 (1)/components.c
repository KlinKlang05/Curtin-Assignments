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
        arr[c] = (int*)calloc(col_num, sizeof(int));
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

void refresh_terminal(int** map, int row_num, int col_num, carPosition car, playerPosition player){
    int c;
    int d;

    for(c = 0; c < row_num; c++){
        for(d = 0; d < col_num; d++){
            if(c == 0 || c == row_num - 1 || d == 0 || d == col_num - 1){
                putchar('*');
            }
            
            else if(player.x == d && player.y == c){
                putchar('P');
            }
            
            else if(car.x == d && car.y == c){
                switch (car.dir){
                case UP:
                    putchar('^');
                    break;

                case RIGHT:
                    putchar('>');
                    break;
                    
                case LEFT:
                    putchar('<');
                    break;

                case DOWN:
                    putchar('v');
                    break;
                }
            }

            else if(map[c][d] == 1 || map[c][d] == 2){
                putchar('.');
            }
            
            else if(map[c][d] == 4){
                putchar('G');
            }
            else{
                putchar(' ');
            }
            
            putchar(' ');
            
        }
        putchar('\n');
    }
    

}

void initialize_positions(int** map, int row_num, int col_num, carPosition* car, playerPosition* player){
    int c; int d;
    car -> dir = RIGHT;

    for(c = 0; c < row_num; c++){
        for(d = 0; d < col_num; d++){
            if(map[c][d] == 3){
                player -> x = d;
                player -> y = c;
            }
            else if(map[c][d] == 2){
                car -> x = d;
                car -> y = c;
            } 
            else if(map[c][d] == 4){
                player -> goalx = d;
                player -> goaly = c;
            }
        }
    }
}

void freeStruct(void* structure){
    free(structure);
}
