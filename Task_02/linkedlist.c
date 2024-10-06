#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Structure to hold student data
struct studentdata {
    int id;
    char name[30];
};

// Node structure for the doubly linked list
typedef struct item {
    struct studentdata a;
    struct item* next;
    struct item* prev;
} item;

// Doubly linked list structure
typedef struct dlink {
    item* head;
    item* tail;
} dlink;

// Function to insert a new node at the head of the list
void insertathead(dlink* list, int id, const char* name) {
    item* new_item = (item*)malloc(sizeof(item));
    if (!new_item) {
        printf("Memory allocation failed\n");
        return;
    }

    new_item->a.id = id;
    strcpy(new_item->a.name, name);
    new_item->next = list->head;
    new_item->prev = NULL;

    if (list->head != NULL) {
        list->head->prev = new_item;
    }
    list->head = new_item;

    if (list->tail == NULL) {
        list->tail = new_item;
    }
}

// Function to display the list
void disp(dlink* list) {
    item* curr = list->head;
    printf("\nThe items from the list are:\n");
    while (curr != NULL) {
        printf("ID: %d, Name: %s\n", curr->a.id, curr->a.name);
        curr = curr->next;
    }
}

// Function to remove a specific node by ID
void removespecific(dlink* list, int id) {
    item* curr = list->head;
    int found = 0;

    while (curr != NULL) {
        if (curr->a.id == id) {
            if (curr == list->head) {
                list->head = curr->next;
                if (list->head != NULL) {
                    list->head->prev = NULL;
                }
            } else if (curr == list->tail) {
                list->tail = curr->prev;
                if (list->tail != NULL) {
                    list->tail->next = NULL;
                }
            } else {
                curr->prev->next = curr->next;
                curr->next->prev = curr->prev;
            }
            free(curr);
            printf("\nItem %d removed from the list\n", id);
            found = 1;
            break;
        }
        curr = curr->next;
    }

    if (!found) {
        printf("\nItem %d not found in the list\n", id);
    }
}

// Function to sort the list using bubble sort
void bubblesort(dlink* list) {
    int swapped;
    item* ptr1;
    item* lptr = NULL;

    if (list->head == NULL)
        return;

    do {
        swapped = 0;
        ptr1 = list->head;

        while (ptr1->next != lptr) {
            if (ptr1->a.id > ptr1->next->a.id) {
                // Swap data
                int temp_id = ptr1->a.id;
                char temp_name[30];
                strcpy(temp_name, ptr1->a.name);

                ptr1->a.id = ptr1->next->a.id;
                strcpy(ptr1->a.name, ptr1->next->a.name);

                ptr1->next->a.id = temp_id;
                strcpy(ptr1->next->a.name, temp_name);

                swapped = 1;
            }
            ptr1 = ptr1->next;
        }
        lptr = ptr1;
    } while (swapped);
}

// Main function
int main() {
    dlink list;
    list.head = NULL;
    list.tail = NULL;

    int id;
    char name[30];

    for (int i = 0; i < 3; i++) {
        printf("\nInsert the student ID: ");
        scanf("%d", &id);
        printf("Insert the student name: ");
        scanf("%s", name);
        insertathead(&list, id, name);
    }

    disp(&list);

    bubblesort(&list);
    printf("\nList after sorting:\n");
    disp(&list);

    printf("\nEnter the ID of the student you want to remove: ");
    scanf("%d", &id);
    removespecific(&list, id);

    printf("\nList after removal:\n");
    disp(&list);

    return 0;
}
