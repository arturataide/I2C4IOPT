/* Net simples_without_net - IOPT */
/* Automatic code generated by IOPT2C XSLT transformation. */


#include <string.h>
#include "net_types.h"


#define ABS(x) (((x)>=0)?(x):-(x))


/* Array implementation: */


void createInitial_simples_without_net_NetMarking( simples_without_net_NetMarking* init_marking )
{
    memset( init_marking, 0, sizeof(*init_marking) );
    init_marking->p_2 = 1; /* Place Place1 */
    init_marking->p_3 = 0; /* Place Place2 */
    init_marking->p_4 = 0; /* Place Place_Cloud2 */
    init_marking->p_5 = 0; /* Place Place_Cloud1 */
}

void createEmpty_simples_without_net_NetMarking( simples_without_net_NetMarking* empty_marking )
{
    empty_marking->p_2 = 0; /* Place Place1 */
    empty_marking->p_3 = 0; /* Place Place2 */
    empty_marking->p_4 = 0; /* Place Place_Cloud2 */
    empty_marking->p_5 = 0; /* Place Place_Cloud1 */
}

void add_simples_without_net_NetMarkings(
    simples_without_net_NetMarking* dest_marking,
    simples_without_net_NetMarking* source_marking )
{
    dest_marking->p_2 += source_marking->p_2; /* Place Place1 */
    dest_marking->p_3 += source_marking->p_3; /* Place Place2 */
    dest_marking->p_4 += source_marking->p_4; /* Place Place_Cloud2 */
    dest_marking->p_5 += source_marking->p_5; /* Place Place_Cloud1 */
}

void init_simples_without_net_OutputSignals(
    simples_without_net_PlaceOutputSignals* place_out,
    simples_without_net_EventOutputSignals* ev_out )
{
    memset( place_out, 0, sizeof(*place_out) );
    memset( ev_out, 0, sizeof(*ev_out) );
    place_out->led1 = 0;
    place_out->led2 = 0;
}

/* Transition 6 - tr_6 */
int t_6_enabled( simples_without_net_NetMarking* prev,
                    simples_without_net_NetMarking* avail )
{
    return ( avail->p_2 >= 1 );
}

int t_6_events( simples_without_net_InputSignalEvents* events )
{
    return ( events->net1E );
}

int t_6_guards( simples_without_net_NetMarking* marking,
                   simples_without_net_InputSignals* inputs,
                   simples_without_net_PlaceOutputSignals* place_out,
                   simples_without_net_EventOutputSignals* ev_out )
{
    return (  1  );
}

void t_6_remove_marks( simples_without_net_NetMarking* marking )
{
    marking->p_2--;
}

void t_6_add_marks( simples_without_net_NetMarking* marking )
{
    marking->p_5++;
}

void t_6_generate_output_events( simples_without_net_OutputSignalEvents* ev_out )
{
}


/* Transition 7 - tr_7 */
int t_7_enabled( simples_without_net_NetMarking* prev,
                    simples_without_net_NetMarking* avail )
{
    return ( avail->p_5 >= 1 );
}

int t_7_events( simples_without_net_InputSignalEvents* events )
{
    return (  1  );
}

int t_7_guards( simples_without_net_NetMarking* marking,
                   simples_without_net_InputSignals* inputs,
                   simples_without_net_PlaceOutputSignals* place_out,
                   simples_without_net_EventOutputSignals* ev_out )
{
    return (  1  );
}

void t_7_remove_marks( simples_without_net_NetMarking* marking )
{
    marking->p_5--;
}

void t_7_add_marks( simples_without_net_NetMarking* marking )
{
    marking->p_3++;
}

void t_7_generate_output_events( simples_without_net_OutputSignalEvents* ev_out )
{
}


/* Transition 8 - tr_8 */
int t_8_enabled( simples_without_net_NetMarking* prev,
                    simples_without_net_NetMarking* avail )
{
    return ( avail->p_3 >= 1 );
}

int t_8_events( simples_without_net_InputSignalEvents* events )
{
    return ( events->net2E );
}

int t_8_guards( simples_without_net_NetMarking* marking,
                   simples_without_net_InputSignals* inputs,
                   simples_without_net_PlaceOutputSignals* place_out,
                   simples_without_net_EventOutputSignals* ev_out )
{
    return (  1  );
}

void t_8_remove_marks( simples_without_net_NetMarking* marking )
{
    marking->p_3--;
}

void t_8_add_marks( simples_without_net_NetMarking* marking )
{
    marking->p_4++;
}

void t_8_generate_output_events( simples_without_net_OutputSignalEvents* ev_out )
{
}


/* Transition 9 - tr_9 */
int t_9_enabled( simples_without_net_NetMarking* prev,
                    simples_without_net_NetMarking* avail )
{
    return ( avail->p_4 >= 1 );
}

int t_9_events( simples_without_net_InputSignalEvents* events )
{
    return (  1  );
}

int t_9_guards( simples_without_net_NetMarking* marking,
                   simples_without_net_InputSignals* inputs,
                   simples_without_net_PlaceOutputSignals* place_out,
                   simples_without_net_EventOutputSignals* ev_out )
{
    return (  1  );
}

void t_9_remove_marks( simples_without_net_NetMarking* marking )
{
    marking->p_4--;
}

void t_9_add_marks( simples_without_net_NetMarking* marking )
{
    marking->p_2++;
}

void t_9_generate_output_events( simples_without_net_OutputSignalEvents* ev_out )
{
}


/* Input event processing: */
void simples_without_net_GenerateInputSignalEvents(
        simples_without_net_InputSignals *old_values,
        simples_without_net_InputSignals *new_values,
        simples_without_net_InputSignalEvents *events )
{
    events->net1E = ( old_values->net1<=0 && new_values->net1>0 );
    events->net2E = ( old_values->net2<=0 && new_values->net2>0 );
}

/* Output event processing: */
void simples_without_net_GenerateEventOutputSignals(
    simples_without_net_OutputSignalEvents *events,
    simples_without_net_EventOutputSignals *signals )
{
}

/* Transition action processing: */
void simples_without_net_GenerateTransitionActionOutputSignals(
    simples_without_net_TransitionFiring *tfired,
    simples_without_net_NetMarking *marking,
    simples_without_net_EventOutputSignals *ev_out )
{
}

/* Place Output Processing */
void simples_without_net_GeneratePlaceOutputSignals(
    simples_without_net_NetMarking *marking,
    simples_without_net_InputSignals *inputs,
    simples_without_net_PlaceOutputSignals *place_out,
    simples_without_net_EventOutputSignals *ev_out )
{
    int exp_res, new_val, n_writes;
    simples_without_net_PlaceOutputSignals new_out = *place_out;
    
    /* Signal led1 */
    new_val = 0;
    if( marking->p_2 > 0 ) { /* Place Place1 */
        exp_res = marking->p_2 == 1;
        if( 1 )
            new_val = exp_res;
    }
    if( new_val > 1 ) new_out.led1 = 1;
    else if( new_val < 0 ) new_out.led1 = 0;
    else new_out.led1 = new_val;

    /* Signal led2 */
    new_val = 0;
    if( marking->p_3 > 0 ) { /* Place Place2 */
        exp_res = marking->p_3 == 1;
        if( 1 )
            new_val = exp_res;
    }
    if( new_val > 1 ) new_out.led2 = 1;
    else if( new_val < 0 ) new_out.led2 = 0;
    else new_out.led2 = new_val;

    *place_out = new_out;
}

