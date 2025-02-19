#ifndef LINKEDLIST_C
#define LINKEDLIST_C

typedef struct node{
    struct node* next;
    struct node* prev;
    void* data;
} NODE;

typedef struct list{
    NODE* HEAD;
    NODE* TAIL;
    int size;

}LinkedList;

typedef void (*listFunc)(void* data);

LinkedList* createLinkedList();
void insertStart(LinkedList* list, void* entry);
void* removeStart(LinkedList* list);
void insertLast(LinkedList* list, void* entry);
void* removeLast(LinkedList* list);
void printLinkedList(LinkedList* list, listFunc funcPtr);
void printStrNode(void* data);
void freeLinkedList(LinkedList* LinkedList, listFunc freeData);

#endif