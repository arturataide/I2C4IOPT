/* Net simples_without_net - IOPT */
/* Automatic code generated by IOPT2C XSLT transformation. */


#include <stdlib.h>
#include <string.h>
#include "net_types.h"


static simples_without_net_TransitionFiring tfired;
    

void simples_without_net_ExecutionStep(
     simples_without_net_NetMarking *prev_marking,
     simples_without_net_InputSignals *inputs,
     simples_without_net_InputSignals *prev_in,
     simples_without_net_PlaceOutputSignals *place_out,
     simples_without_net_EventOutputSignals *ev_out )
{
    simples_without_net_NetMarking add_marking;
    simples_without_net_NetMarking avail_marking = *prev_marking;
    simples_without_net_InputSignalEvents input_events;
    simples_without_net_OutputSignalEvents output_events;

    memset( &output_events, 0, sizeof(output_events) );
    memset( &tfired, 0, sizeof(tfired) );

    createEmpty_simples_without_net_NetMarking( &add_marking );
    simples_without_net_GetInputSignals( inputs, &input_events );
    simples_without_net_GenerateInputSignalEvents( prev_in, inputs, &input_events );
    *prev_in = *inputs;

    /* Transition tr_7 */
    if( t_7_enabled( prev_marking, &avail_marking ) &&
        t_7_events( &input_events ) &&
        t_7_guards( prev_marking, inputs, place_out, ev_out ) ) {
        tfired.t_7 = 1;
        t_7_remove_marks( &avail_marking );
        t_7_add_marks( &add_marking );
        t_7_generate_output_events( &output_events );
    }

    /* Transition tr_9 */
    if( t_9_enabled( prev_marking, &avail_marking ) &&
        t_9_events( &input_events ) &&
        t_9_guards( prev_marking, inputs, place_out, ev_out ) ) {
        tfired.t_9 = 1;
        t_9_remove_marks( &avail_marking );
        t_9_add_marks( &add_marking );
        t_9_generate_output_events( &output_events );
    }

    add_simples_without_net_NetMarkings( &avail_marking, &add_marking );

    simples_without_net_GenerateTransitionActionOutputSignals( &tfired, &avail_marking, ev_out );
    simples_without_net_GeneratePlaceOutputSignals( &avail_marking, inputs, place_out, ev_out );
    simples_without_net_GenerateEventOutputSignals( &output_events, ev_out );
    simples_without_net_PutOutputSignals( place_out, ev_out, &output_events );
    *prev_marking = avail_marking;
}

simples_without_net_TransitionFiring* get_simples_without_net_TransitionFiring()
{
    return &tfired;
}
