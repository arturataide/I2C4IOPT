/* Net simples_without_net - IOPT */
/* Automatic code generated by IOPT2C XSLT transformation. */
/* Please fill the necessary code to perform hardware IO. */


#include <stdlib.h>
#include "net_types.h"


#ifdef ARDUINO
#include <Arduino.h>
#define ANALOG_IN_MAX  1023
#define ANALOG_OUT_MAX 255
#else
#define INPUT    0
#define OUTPUT   1
#define ANALOG_IN_MAX  1023
#define ANALOG_OUT_MAX 1023
extern void pinMode( int, int );
extern int  digitalRead( int );
extern void digitalWrite( int, int );
extern int  analogRead( int );
extern void analogWrite( int, int );
#endif


// Remote IcE/Debug forced values:
#ifdef HTTP_SERVER
iopt_param_info *input_fv = NULL, *output_fv = NULL;
#endif


/* Executed just once, before net execution starts: */
void simples_without_net_InitializeIO()
{
    //PYTHON - Initialize digital outputs
    pinMode(2, OUTPUT);
    digitalWrite(2, LOW);
    pinMode(3, OUTPUT);
    digitalWrite(3, LOW);
    pinMode(4, OUTPUT);
    digitalWrite(4, LOW);
    pinMode(5, OUTPUT);
    digitalWrite(5, LOW);
    pinMode(6, OUTPUT);
    digitalWrite(6, LOW);
    pinMode(7, OUTPUT);
    digitalWrite(7, LOW);
    pinMode(8, OUTPUT);
    digitalWrite(8, LOW);
    pinMode(9, OUTPUT);
    digitalWrite(9, LOW);
    pinMode(10, OUTPUT);
    digitalWrite(10, LOW);
    pinMode(11, OUTPUT);
    digitalWrite(11, LOW);
    pinMode(12, OUTPUT);
    digitalWrite(12, LOW);
    pinMode(13, OUTPUT);
    digitalWrite(13, LOW);
}



/* Read all hardware input signals and fill data-structure */
void simples_without_net_GetInputSignals(
            simples_without_net_InputSignals* inputs,
            simples_without_net_InputSignalEvents* events )
{
    inputs->net1 = 0;
    inputs->net2 = 0;
    //PYTHON - Digital read the inputs
    inputs->net1 = digitalRead(2);
    inputs->net2 = digitalRead(3);
    //PYTHON - End digital read the inputs
#ifdef HTTP_SERVER
    if( input_fv != NULL ) force_simples_without_net_Inputs( input_fv, inputs );
#endif
}


/* Write all output values to physical hardware outputs */
void simples_without_net_PutOutputSignals(
            simples_without_net_PlaceOutputSignals* place_out,
            simples_without_net_EventOutputSignals* event_out,
            simples_without_net_OutputSignalEvents* events )
{
#ifdef HTTP_SERVER
    if( output_fv != NULL )
        force_simples_without_net_Outputs( output_fv, place_out, event_out );
#endif
    /* place_out->led1 */
    /* place_out->led2 */
    //PYTHON - Digital write the outputs
    digitalWrite(4, place_out->led1);
    digitalWrite(5, place_out->led2);
    //PYTHON - End digital write the outputs
}


/* Delay between loop iterations to save CPU and power consumption */
void simples_without_net_LoopDelay()
{
    //PYTHON - Loop config
    delay(10);
    Serial.println("Loop");
    //PYTHON - End loop config
}

/* Must return 1 to finish net execution */
int simples_without_net_FinishExecution( simples_without_net_NetMarking* marking )
{
    return 0;
}



