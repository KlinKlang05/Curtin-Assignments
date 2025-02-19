#include <stdio.h>
#include <stdlib.h>
#include "components.h"
#include "updates.h"
#include "linkedList.h"
/*#include "updates.h"*/

int main(int argc, char* argv[]){
    char* filename = argv[1];
    int rowCount; int colCount;
    int actualRowCount; int actualColCount;
    int filestate;
    int** board;
    int i; int j;
    carPosition mainCar; playerPosition mainPlayer;
    LinkedList* playerHistory = createLinkedList(); LinkedList* carHistory = createLinkedList();
    
    if(argc == 1){
        printf("Please specify a file path!\n\n");
    }
    else
    {
        FILE* f = fopen(filename, "r");

        if(f == NULL){
            perror("Could not open file.");
        } else{
            filestate = fscanf(f, "%d %d", &rowCount, &colCount);

            if(filestate == EOF){
                printf("The file exists but is empty.");
            } else{

                actualRowCount = rowCount + 2; /*Add 2 to account for borders*/
                actualColCount = colCount + 2; /*Add 2 to account for borders*/

                board = initialize_2d_int_array(actualRowCount, actualColCount); /*Need to free*/ 
                for(i=0; i<rowCount; i++){
                    for(j=0; j<colCount; j++){
                        filestate = fscanf(f, "%d ", board[i+1] + j+1);
                    }
                }

                initialize_positions(board, actualRowCount, actualColCount, &mainCar, &mainPlayer);
                main_loop(board, &mainPlayer, &mainCar, actualRowCount, actualColCount, carHistory, playerHistory);

            }

            fclose(f);
            free_2d_int_array(board, actualRowCount);
            freeLinkedList(carHistory, freeStruct);
            freeLinkedList(playerHistory, freeStruct);
        }
    }
    
    

    return 0;
}