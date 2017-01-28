#!/usr/bin/python

import sys, getopt, re

class AddSerialToCode:

    def __init__(self, input_file, output_file):
        '''
            Initialize AddSerialToCode object
            @param input_file file to be read
            @param output_file file to write the new code
        '''

        self.input_file    = input_file
        self.output_file   = output_file
        self.input_events  = []
        self.output_events = []
        self.outputs       = []
        # TODO missing inputs
        self.DIGITAL_PORTS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.TAB           = "    "

    def write(self):
        '''
            Write the SoftwareSerial communication code to the output file
        '''

        try:
            # open input file to read and output file to append
            f_read  = open(self.input_file, 'r')
            f_write = open(self.output_file, 'w')
            # get the number of places, events and signals and go to the start of the file
            self.count_events_and_places(f_read.read())
            f_read.seek(0, 0)
            for index, line in enumerate(f_read):
                f_write.write(line)

                if index == 34: # Initialize digital ouputs and serial communications
                    f_write.write(self.TAB + '//PYTHON - Initialize digital outputs\n')
                    for k in range(len(self.DIGITAL_PORTS)):
                        f_write.write(self.TAB + 'pinMode(' + str(self.DIGITAL_PORTS[k]) + ', OUTPUT);\n')
                        f_write.write(self.TAB + 'digitalWrite(' + str(self.DIGITAL_PORTS[k]) + ', LOW);\n')

                if index == 45: # Initialize digital ouputs and serial communications
                    f_write.write(self.get_inputs_places_string())

                if index == 63: # Write digital outputs
                    f_write.write(self.get_output_places_string())

                if index == 69: # Loop config
                    f_write.write(self.TAB + '//PYTHON - Loop config\n' +
                                  self.TAB + 'delay(10);\n' +
                                  self.TAB + 'Serial.println("Loop");\n' +
                                  self.TAB + '//PYTHON - End loop config\n')


        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except ValueError:
            print "Could not convert data to an integer."
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise


    def get_events_flags_str(self):
        string = ''
        for i in self.input_events:
            string += 'int ' + i + '_flag = 0;\n'
        return string

    def get_receive_string_verification(self):
        string = ''
        for i in self.input_events:
            string += self.TAB + 'if(readString == "' + i + '") {\n' +\
                       self.TAB + self.TAB + i + '_flag = 1;\n' +\
                        self.TAB + '}'
        return string

    def get_event_flag_check_string(self):
        string = self.TAB + self.TAB + '// PYTHON - Change event state\n'
        for i in self.input_events:
            string += self.TAB + self.TAB + 'if (' + i + '_flag) {\n' +\
                      self.TAB + self.TAB + self.TAB + 'events->' + i + ' = 1;\n' +\
                      self.TAB + self.TAB + self.TAB + i + '_flag = 0;\n' +\
                      self.TAB + self.TAB + '} else {\n' +\
                      self.TAB + self.TAB + self.TAB + 'events->'+ i + ' = 0;\n' +\
                      self.TAB + self.TAB + '}\n'
        string += self.TAB + self.TAB + '//PYTHON - End change event state\n'
        return string

    def get_inputs_places_string(self):
        string = self.TAB + '//PYTHON - Digital read the inputs\n'
        for i, item in enumerate(self.inputs):
            string += self.TAB + 'inputs->' + item + ' = digitalRead(' + str(self.DIGITAL_PORTS[i]) + ');\n'
        string += self.TAB + '//PYTHON - End digital read the inputs\n'
        return string

    def get_output_places_string(self):
        string = self.TAB + '//PYTHON - Digital write the outputs\n'
        for i, item in enumerate(self.outputs):
            string += self.TAB + 'digitalWrite(' + str(self.DIGITAL_PORTS[i + len(self.inputs)]) + ', place_out->' + item + ');\n'
        string += self.TAB + '//PYTHON - End digital write the outputs\n'
        return string



    def count_events_and_places(self, file_content):
        '''
            Method to count the number of events in this net
            @param file_content content of the input file`
            @return number of events in this net
        '''
       
        
        input_digital_string = re.findall(r'.InputSignalEvents(.*)input_fv != NULL.*', file_content, re.S)
        self.inputs = re.findall(r'inputs->(.*) = 0;', input_digital_string[0])
        print "\nInputs"
        for i, item in enumerate(self.inputs):
            print 'Digital ' + str(self.DIGITAL_PORTS[i]) + " -> " + item
        print len(self.inputs)        

        #output events string        
        output_events_string = re.findall(r'.OutputSignalEvents(.*)LoopDelay().*', file_content, re.S)
        self.outputs = re.findall(r'place_out->(.*) \*\/', output_events_string[0][0])        
        print "\nOutputs: "
        for i, item in enumerate(self.outputs):
            print 'Digital ' + str(self.DIGITAL_PORTS[i + len(self.inputs)]) + " -> " + item        
        print len(self.outputs)
        
        # input events string
        input_events_string = re.findall(r'.GetInputSignals\(.*events != NULL(.*)input_fv != NULL.*', file_content, re.S)                        
        print "\nInput Events: "
        if len(input_events_string) > 0:
            self.input_events = re.findall(r'events->(.*) \*\/', input_events_string[0])
        print self.input_events
        print len(self.input_events)

        print "\nOutput Events: "
        self.output_events = re.findall(r'events->(.*) \*\/', output_events_string[0][0])
        print self.output_events
        print len(self.output_events)

if __name__ == "__main__":
    '''
        Get args from console
        @param -i input file
        @param -o output file
        @param -h show help text
    '''

    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'write_file.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    # Create object to add SoftwareSerial code and communication
    addSerialToCode = AddSerialToCode(inputfile, outputfile)
    addSerialToCode.write()

