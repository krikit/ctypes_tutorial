#include <stdlib.h>
#include "mylib.h"

/* set value as 0 and next pointer as NULL */
void init_node(node_t* node) {
    if (node == NULL) return;
    node->value = 0;
    node->next = NULL;
}

/* make liked list of 'num' number of nodes and return its head node */
node_t* make_list(int num) {
    node_t* head = NULL;
    node_t* curr = NULL;
    int cnt = 0;

    if (num == 0) return NULL;

    head = (node_t*) malloc(sizeof(node_t));
    init_node(head);
    head->value = 1;

    curr = head;
    for (cnt = 1; cnt < num; ++cnt) {
        curr->next = (node_t*) malloc(sizeof(node_t));
        init_node(curr->next);
        curr->next->value = cnt + 1;
        curr = curr->next;
    }

    return head;
}

/* delete node itself and next pointer recursively */
void del_list(node_t* head) {
    if (head == NULL) return;
    if (head->next != NULL) del_list(head->next);
    free(head);
}
