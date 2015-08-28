#ifndef __MYLIB_H__
#define __MYLIB_H__

#ifdef __cplusplus__
extern "C" {
#endif

/* node data structure of linked list */
typedef struct _node_t {
  int value;
  struct _node_t* next;
} node_t;

void init_node(node_t* node);    /* initialize node */
node_t* make_list(int num);      /* make list of 'num' numbers */
void del_list(node_t* head);     /* delete entire nodes in list */

#ifdef __cplusplus__
}
#endif

#endif    // __MYLIB_H__
