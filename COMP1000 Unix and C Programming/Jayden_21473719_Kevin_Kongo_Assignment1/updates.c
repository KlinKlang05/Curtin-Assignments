#include <stdio.h>
#include <stdlib.h>
#include "updates.h"

static int finish_condition(int* player, int** cars, int num_cars, int num_row, int num_col);

void main_loop(char** map, int** car_array, int num_row, int num_col, int car_count){
    int player_coords[2] = {1, 1}; /*Initial player coordinates on the map*/
    int i; 
    char input;

    refresh_map_array(map, num_row, num_col); /*Call once before mainloop to initialize the map, so that first print is not blank*/
    initialize_cars(car_array, map, car_count, num_row, num_col); /*Call once to randomly generate initial car positions*/
    map[player_coords[0]][player_coords[1]] = 'P'; /*Place Player onto map array*/

    system("clear");
    for(i = 0; i < num_row; i++){ /*Print the initial state of the map before first move*/
            printf("%s", map[i]); 
    }
    printf("w -> up\na -> left\ns -> down\nd -> right\n");

    do{                    
        disableBuffer();
        scanf(" %c", &input); /*Take input with buffer disabled*/
        enableBuffer();
        if(input == 'w' || input == 'a' || input == 's' || input == 'd'){
            refresh_map_array(map, num_row, num_col); /*clean map to remove old car and player positions*/
            update_cars(map, car_array, car_count, num_row, num_col); /*Update cars, then player, so that the player is always printed on top of the car if they happen to be bad enough to hit one.*/
            update_player(map, player_coords, num_row-2, num_col-4, input);

            system("clear"); /*Wipe previous frame*/

            #ifdef DEBUG
            printf("%d, %d\n\n", player_coords[0], player_coords[1]);
            #endif

            for(i = 0; i < num_row; i++){ /*Reprint updated map*/

                #ifdef DEBUG
                printf("%d", i);
                #endif

                printf("%s", map[i]); 
            }
            printf("w -> up\na -> left\ns -> down\nd -> right\n");
        }

    }while(finish_condition(player_coords, car_array, car_count, num_row, num_col)); /*Run function every loop to check if player is in losing position*/
}

void update_player(char** map, int* coords, int num_row, int num_col, char input){
    switch (input){  /*Update player coordinates based on keyboard input*/
        case 'w':
            if(coords[0] != 1){
                coords[0] -= 1;
            }
        break;
        case 'a':
            if(coords[1] != 1){
                coords[1] -= 1;
            }
        break;
        case 's':
            if(coords[0] != num_row){
                coords[0] = coords[0] + 1;
            }
        break;
        case 'd':
            if(coords[1] != num_col){
                coords[1] += 1;
            }
        break;
    }
    map[coords[0]][coords[1]] = 'P'; /*Add new player location*/
}


void update_cars(char** map, int** car_array, int car_count, int num_row, int num_col){
    int i; 
    char dir;

    for(i=0; i<car_count; i++){ 
        if(car_array[i][2] == 0){ /*Move car left/right depending on direction*/
            car_array[i][1] -= 1;
        }
        else{
            car_array[i][1] += 1;
        }
        if(car_array[i][1] == 1 || car_array[i][1] == num_col - 4){ /*Change direction of car if it is now on border*/
            car_array[i][2] = !car_array[i][2];
        }

        if(car_array[i][2] == 0){   
            dir = '<';
        }else{
            dir = '>';
        }
        map[car_array[i][0]][car_array[i][1]] = dir; /*Place car onto the array*/
    }
}

static int finish_condition(int* player, int** cars, int num_cars, int num_row, int num_col){
    int cond = 1;
    int i;
    char *msg;

    for(i=0; i<num_cars; i++){ /*If the player lands on a car, turn cond to false (0) and print losing message*/
        if(player[0] == cars[i][0] && player[1] == cars[i][1]){
            cond = !cond;
            msg = "\nYou lose!\n\n";
        }
    }

    if(player[0] == num_row - 2 && player[1] == num_col - 4){ /*If the player lands on the goal, turn cond to false (0) and print winning message*/
            cond = !cond;
            msg = "\nYou win!\n\n";
    }

    if(!cond){
        printf("%s", msg);
    }
    return cond;
}