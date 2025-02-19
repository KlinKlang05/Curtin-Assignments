#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "updates.h"
#define DEBUG_OFF


static int finish_condition(playerPosition player, carPosition car, int num_row, int num_col){
    int cond = 1;
    char *msg;

    if(player.x == car.x && player.y == car.y){/*If the player lands on the car, turn cond to false (0) and print losing message*/
        cond = !cond;
        msg = "\nYou lose!\n\n";
    }

    if(player.x == player.goalx && player.y == player.goaly){ /*If the player lands on the goal, turn cond to false (0) and print winning message*/
            cond = !cond;
            msg = "\nYou win!\n\n";
    }

    if(!cond){
        printf("%s", msg);
    }
    return cond;
}

static Direction check_horizontal(int** map, int x, int y){
    if(map[y][x+1] == 1 || map[y][x+1] == 2){ /*Check right*/
        return RIGHT;
    }else{ /*Otherwise it must be left*/
        return LEFT;
    }
}

static Direction check_vertical(int** map, int x, int y){
    if(map[y-1][x] == 1 || map[y-1][x] == 2){ /*Check up*/
        return UP;
    }else{ /*Otherwise it must be down*/
        return DOWN;
    }
}

static void move_car(carPosition* car, Direction dir){
    switch (dir){
        case UP:
            car->y -= 1;
        break;
        case DOWN:
            car->y += 1;
        break;
        case LEFT:
            car->x -= 1;
        break;
        case RIGHT:
            car->x += 1;
        break;
    }
}

void main_loop(int** map, playerPosition* player, carPosition* car, int num_row, int num_col, LinkedList* carHistory, LinkedList* playerHistory){
    char input;
    playerPosition* playerTemp;
    carPosition* carTemp;

    #ifdef DEBUG
    int i; int j;
    #endif  

    system("clear");
    #ifdef DEBUG
            printf("player: %d, %d\n", player->x, player->y);
            printf("car: %d, %d\n", car->x, car->y);
            printf("value next to car: above:%d below:%d right:%d left:%d\n", map[car->x][car->y-1], map[car->x][car->y+1], map[car->x-1][car->y], map[car->x-1][car->y]);
            printf("u0/r1/l2/d3: %d", car->dir);
            printf("%d\n", num_row);
            printf("%d\n", num_col);
    #endif
    refresh_terminal(map, num_row, num_col, *car, *player);     /*Print the initial state of the map before first move*/


    printf("w -> up\na -> left\ns -> down\nd -> right\nu -> undo");

    do{                    
        disableBuffer();
        scanf(" %c", &input); /*Take input with buffer disabled*/
        enableBuffer();
        
        if(input == 'w' || input == 'a' || input == 's' || input == 'd'){
            playerTemp = (playerPosition*)malloc(sizeof(playerPosition));
            carTemp = (carPosition*)malloc(sizeof(carPosition));
            *playerTemp = *player;
            *carTemp = *car;

            update_car(map, car);
            update_player(player, input, num_row, num_col);

            insertLast(playerHistory, playerTemp);
            insertLast(carHistory, carTemp);
            system("clear"); /*Wipe previous frame*/
           
        }
        else if(input == 'u' && playerHistory->size != 0 && carHistory->size != 0){
            
            carTemp = removeLast(carHistory);
            playerTemp = removeLast(playerHistory);
            *car = *carTemp;
            *player = *playerTemp;

            free(carTemp);   /*After values are retrieved from the linked list and copied back to the main structs, the malloced struct that stored the copies must be freed.*/
            free(playerTemp);
            system("clear"); /*Wipe previous frame*/
        }
        else if(input == 'u'){
            system("clear"); /*Wipe previous frame*/
            printf("\nThere is no remaining history to undo! \n");
            
        }

        #ifdef DEBUG
            printf("player: %d, %d\n", player->x, player->y);
            printf("car: %d, %d\n", car->x, car->y);
            /*printf("value next to car: above:%d below:%d right:%d left:%d\n", map[car->x][car->y-1], map[car->x][car->y+1], map[car->x-1][car->y], map[car->x-1][car->y]);*/
            printf("u0/r1/l2/d3: %d", car->dir);
            printf("%d\n", num_row);
            printf("%d\n", num_col);

        #endif
        refresh_terminal(map, num_row, num_col, *car, *player);  /*Reprint updated map*/
        printf("w -> up\na -> left\ns -> down\nd -> right\nu -> undo");

    }while(finish_condition(*player, *car, num_row, num_col)); /*Run function every loop to check if player is in losing position*/
}

void update_player(playerPosition* player, char input, int num_row, int num_col){
    switch (input){  /*Update player coordinates based on keyboard input*/
        case 'a':
            if(player -> x != 1){
                player -> x -= 1;
            }
        break;
        case 'w':
            if(player -> y != 1){
                player -> y -= 1;
            }
        break;
        case 'd':
            if(player -> x != num_col-2){
                player -> x += 1;
            }
        break;
        case 's':
            if(player -> y != num_row-2){
                player -> y += 1;
            }
        break;
    }
}



void update_car(int** map, carPosition* car){
    switch (car->dir){
        case UP:
            if(map[car->y-1][car->x] == 1 || map[car->y-1][car->x] == 2){
                move_car(car, UP);
            }
            else{
                car -> dir = check_horizontal(map, car->x, car->y);
                move_car(car, car->dir);
            }
        break;
        case DOWN:
            if(map[car->y+1][car->x] == 1 || map[car->y+1][car->x] == 2){
                move_car(car, DOWN);
            }
            else{
                car -> dir = check_horizontal(map, car->x, car->y);
                move_car(car, car->dir);
            }
        break;
        case LEFT:
            if(map[car->y][car->x-1] == 1 || map[car->y][car->x-1] == 2){
                    move_car(car, LEFT);
            }
            else{
                car -> dir = check_vertical(map, car->x, car->y);
                move_car(car, car->dir);
            }
        break;
        case RIGHT:
            if(map[car->y][car->x+1] == 1 || map[car->y][car->x+1] == 2){
                    move_car(car, RIGHT);
            }
            else{
                car -> dir = check_vertical(map, car->x, car->y);
                move_car(car, car->dir);
            }
        break;
    }
    
}

