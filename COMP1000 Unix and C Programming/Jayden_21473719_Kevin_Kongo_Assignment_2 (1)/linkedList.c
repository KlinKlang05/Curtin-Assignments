#include <stdlib.h>
#include <stdio.h>  
#include "linkedlist.h"



LinkedList* createLinkedList(){
    LinkedList* list = (LinkedList*)malloc(sizeof(LinkedList));
    list->HEAD = NULL;
    list->TAIL = NULL;
    list->size = 0;

    return list;
}

void insertStart(LinkedList* list, void* entry){
    NODE* insert = (NODE*)malloc(sizeof(NODE));
    insert->data = entry;
    insert->next = NULL;
    insert->prev = NULL;

    if(list->HEAD == NULL){
        list->HEAD = insert;
        list->TAIL = insert;
    }
    else if(list->HEAD == list->TAIL){
        list->TAIL->prev = insert;
        list->HEAD = insert;
        list->HEAD->next = list->TAIL;
    }
    else{
        NODE* curr = list->HEAD;
        list->HEAD = insert;
        list->HEAD->next = curr;
        curr->prev = list->HEAD;
    }
    list->size += 1;
}

void* removeStart(LinkedList* list){
    void* ret = NULL;
    NODE* curr = list->HEAD;                  
    
    if(curr != NULL){
        ret = curr->data;
        if(curr->next != NULL){
            curr->next->prev = NULL;
            list->HEAD = curr->next;
        }
        else{
            list->HEAD = NULL;
            list->TAIL = NULL;
        }
        list->size -= 1;
    }
    free(curr);
    return ret;
}

void insertLast(LinkedList* list, void* entry){
    NODE* insert = (NODE*)malloc(sizeof(NODE));
    insert->data = entry;
    insert->next = NULL;
    insert->prev = NULL;

    if(list->TAIL == NULL){
        list->HEAD = insert;
        list->TAIL = insert;
    }
    else if(list->TAIL == list->HEAD){
        list->HEAD->next = insert;
        list->TAIL = insert;
        list->TAIL->prev = list->HEAD;
    }
    else{
        NODE* curr = list->TAIL;
        list->TAIL = insert;
        list->TAIL->prev = curr;
        curr->next = list->TAIL;
    }
    list->size += 1;
}

void* removeLast(LinkedList* list){
    void* ret = NULL;
    NODE* curr = list->TAIL;        
    
    if(curr != NULL){
        ret = curr->data;
        if(curr->prev != NULL){
            curr->prev->next = NULL;
            list->TAIL = curr->prev;
        }
        else{
            list->TAIL = NULL;
            list->HEAD = NULL;
        }
        list->size -= 1;
    }
    free(curr);

    return ret;
}

void printLinkedList(LinkedList* list, listFunc funcPtr){
    NODE* curr = list->HEAD;
    while(curr != NULL){
        funcPtr(curr->data);
        curr = curr->next;
    }
}

void freeLinkedList(LinkedList* LinkedList, listFunc freeData){
    NODE* curr = LinkedList->HEAD;
    NODE* next;
    while(curr != NULL){
        next = curr->next;
        freeData(curr->data);
        free(curr);
        curr = next;
    }
    free(LinkedList);
}

void printStrNode(void* data){
    printf("%s", (char*)data);
    printf("\n");
}
