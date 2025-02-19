#include <stdio.h>
#include <stdlib.h>
#include "components.h"
#include "updates.h"

int main(int argc, char* argv[]){
    int rows;
    int cols;
    int car_count;

    if(argc == 1 || argc > 3){
        printf("Usage: ./cars <map_row> <map_col>\n\n");
    } 
    else {
        rows = atoi(argv[1]) + 2; /*Add 2 to account for borders*/
        cols = atoi(argv[2]) + 4; /*Add 4 to account for borders, newline and null character*/
        car_count = (rows - 1 - 2) / 2;

        if(rows-2 < 3 || (rows-2) % 2 == 0){
        printf("\nThe row argument must be greater than three, and an odd number.\n\n");
        } 

        else if(cols-4 < 5){
        printf("\nThe column argument must be greater than five.\n\n");
        }

        else{
            char** map = initialize_2d_char_array(rows, cols);
            int** cars = initialize_2d_int_array(car_count, 3); /*number of rows equals number of cars, columns equals row, col position and direction*/

            main_loop(map, cars, rows, cols, car_count);

            free_2d_char_array(map, rows);
            free_2d_int_array(cars, car_count);

        }
    }
    return 0;
}