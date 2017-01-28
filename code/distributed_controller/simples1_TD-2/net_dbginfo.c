/* Net simples_without_net - IOPT */
/* Automatic code generated by IOPT2C XSLT transformation. */


#include <string.h>
#include <stdlib.h>
#include "net_types.h"


#if defined(HTTP_SERVER) || defined(DBG_INFO)

static iopt_param_info simples_without_net_input_info[] = {
    { "net1", 0 },
    { "net2", 0 },
    { NULL, 0 }
};

static iopt_param_info simples_without_net_output_info[] = {
    { "led1", 0 },
    { "led2", 0 },
    { NULL, 0 }
};

static iopt_param_info simples_without_net_marking_info[] = {
    { "p_3", 0 },
    { NULL, 0 }
};

static iopt_param_info simples_without_net_tfired_info[] = {
    { "t_8", 0 },
    { "t_10", 0 },
    { NULL, 0 }
};

iopt_param_info* get_simples_without_net_InputInfo()
{
    simples_without_net_InputSignals* inputs = get_simples_without_net_InputSignals();
    simples_without_net_input_info[0].value = inputs->net1;
    simples_without_net_input_info[1].value = inputs->net2;
    return simples_without_net_input_info;
}

iopt_param_info* get_simples_without_net_OutputInfo()
{
    simples_without_net_PlaceOutputSignals* place_out = get_simples_without_net_PlaceOutputSignals();
    simples_without_net_EventOutputSignals* ev_out = get_simples_without_net_EventOutputSignals();
    simples_without_net_output_info[0].value = ev_out->led1;
    simples_without_net_output_info[1].value = place_out->led2;
    return simples_without_net_output_info;
}

iopt_param_info* get_simples_without_net_MarkingInfo()
{
    simples_without_net_NetMarking* marking = get_simples_without_net_NetMarking();
    simples_without_net_marking_info[0].value = marking->p_3;
    return simples_without_net_marking_info;
}

void force_simples_without_net_Inputs( iopt_param_info fv[],
        simples_without_net_InputSignals* in )
{
    int i;
    for( i = 0; fv[i].name != NULL; ++i ) {
        if( strcmp( fv[i].name, simples_without_net_input_info[0].name ) == 0 )
           in->net1 = fv[i].value;
        else if( strcmp( fv[i].name, simples_without_net_input_info[1].name ) == 0 )
           in->net2 = fv[i].value;
    }
}

void force_simples_without_net_Outputs( iopt_param_info fv[],
        simples_without_net_PlaceOutputSignals* place_out,
        simples_without_net_EventOutputSignals* ev_out )
{
    int i;
    for( i = 0; fv[i].name != NULL; ++i ) {
        if( strcmp( fv[i].name, simples_without_net_output_info[0].name ) == 0 )
           ev_out->led1 = fv[i].value;
        else if( strcmp( fv[i].name, simples_without_net_output_info[1].name ) == 0 )
           place_out->led2 = fv[i].value;
    }
}

void force_simples_without_net_Marking( iopt_param_info fv[],
        simples_without_net_NetMarking* m )
{
    int i;
    for( i = 0; fv[i].name != NULL; ++i ) {
        if( strcmp( fv[i].name, simples_without_net_marking_info[0].name ) == 0 )
           m->p_3 = fv[i].value;
    }
}

iopt_param_info* get_simples_without_net_TFiredInfo()
{
    simples_without_net_TransitionFiring* tfired = get_simples_without_net_TransitionFiring();
    simples_without_net_tfired_info[0].value = tfired->t_8;
    simples_without_net_tfired_info[1].value = tfired->t_10;
    return simples_without_net_tfired_info;
}

#endif
