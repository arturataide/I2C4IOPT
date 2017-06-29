# compile python setup.py py2app -A
# run ./dist/main.app/Contents/MacOS/main
from Cocoa import *
from Foundation import NSObject
import glob, zipfile, os, os.path, re

class MainController(NSWindowController):
    filesCounter   = objc.IBOutlet()
    fileNames      = objc.IBOutlet()
    addressesLabel = objc.IBOutlet()
    readyLabel     = objc.IBOutlet()

    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)
        # init variables
        #self.DIR = '/Users/arturataide/Desktop/IOPT2AC_tool/zip_files/'
        self.DIR = '../../../../zip_files/'
        self.modelsNumber = "Not verified yet."
        self.names = ""
        self.models = []
        self.count_files()
        self.dirs = []
        print("AddSerialToCode")

        self.model_name    = ""
        self.input_events  = []
        self.output_events = []
        self.outputs       = []
        self.DIGITAL_PORTS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.TAB           = "    "
        self.addresses     = []
        self.strings = {}

    @objc.IBAction
    def countFiles_(self, sender):
        self.count_files()

    def count_files(self):
        # count zip files in folder
        files = len(glob.glob(self.DIR + '*.zip'))
        self.modelsNumber = "There are " + str(files) + " compressed models."
        print(self.modelsNumber)
        self.updateDisplay()

    @objc.IBAction
    def unzipFiles_(self, sender):
        self.addresses = []
        self.ready_str = ""
        self.updateReadyLabel()
        self.dirs = []
        self.models = []
        self.names = ""
        # unzip files
        files = glob.glob(self.DIR + '*.zip')
        for f in files:
            zip_ref = zipfile.ZipFile(f, 'r')
            zip_ref.extractall(self.DIR)
            zip_ref.close()
        # get unziped file dirs and prepare I2C addresses
        dirs_temp = filter(os.path.isdir, [os.path.join(self.DIR,f) for f in os.listdir(self.DIR)])
        for d in dirs_temp:
            name = d.split('/')[-1]
            self.dirs.append(name)
            self.names += name + "\n"
        # update interface
        # remove unused files and rename main file
        self.removeUnusedFiles()
        #self.prepare addresses
        self.prepareAddresses()
        self.updateUnzippedFiles()
        self.write_IO_files()

    def removeUnusedFiles(self):
        # remove unused and rename main file to *.ino
        print('Removing and Renaming files...')
        for d in self.dirs:
            os.remove(self.DIR + d + '/MakeFile')
            os.remove(self.DIR + d + '/http_server.h')
            os.remove(self.DIR + d + '/http_server.c')
            os.remove(self.DIR + d + '/dummy_gpio.c')
            os.remove(self.DIR + d + '/linux_sys_gpio.c')
            os.remove(self.DIR + d + '/raspi_mmap_gpio.c')
            os.remove(self.DIR + d + '/net_dbginfo.c')
            os.remove(self.DIR + d + '/net_server.h')
            os.remove(self.DIR + d + '/net_server.c')
            path_name = '/' + d.split('/')[-1]
            os.rename(self.DIR + d + '/net_main.c', self.DIR + d + path_name + '.ino')
        print('Done\n')

    def prepareAddresses(self):
        print("Preparing addresses")
        self.names = ""
        for d in self.dirs:
            self.input_file = self.DIR + d + '/net_io.c'
            print("Preparing addresses in " + self.input_file)
            events = self.get_all_outputs()
            name = d.split('/')[-1]
            model = {
                    'address': hex(len(self.models) + 1),
                    'model': name,
                    'events': events
            }
            self.names += model['model'] + " -> " + model['address'] + "\n"
            self.models.append(model)
        print("Done")

    def write_IO_files(self):
        print("Writing files")
        i = 0
        for d in self.dirs:

            _input = self.DIR + d + '/net_io.c'
            _output = self.DIR + d + '/net_io.cpp'
            print(_input)
            print(_output)
            #addSerialToCode = IOPT2AC_distributed.AddSerialToCode(_input, _output, self.models[i]['address'], self.models)
            print("to write")
            self.input_file    = _input
            self.output_file   = _output
            self.this_address = self.models[i]['address']
            self.write()
            i += 1
            os.remove(_input)
            #self, input_file, output_file, address, models):
        print("Done, Ready to run in Arduino")
        self.ready_str = "Models are ready to be burned in Arduino"
        self.updateReadyLabel()



    # update interfaces
    def updateDisplay(self):
        self.filesCounter.setStringValue_(self.modelsNumber)

    def updateUnzippedFiles(self):
        self.fileNames.setStringValue_(self.names)

    def updateAddressesLabel(self):
        self.addressesLabel.setStringValue_("".join(str(self.addresses).split()))

    def updateReadyLabel(self):
        self.readyLabel.setStringValue_(self.ready_str)


    # Write to file IOPT2AC_distributed
    def write(self):
        '''
            Write the SoftwareSerial communication code to the output file
        '''
        print(self.input_file)
        print(self.output_file)
        try:
            print(self.input_file)
            print(self.output_file)
            # open input file to read and output file to append
            f_read  = open(self.input_file, 'r')
            f_write = open(self.output_file, 'w')
            # get the number of places, events and signals and go to the start of the file
            self.file_content = f_read.read()
            self.get_file_data()
            self.ask_for_addresses()
            print("INIT WRITING TO FILE")
            f_write.write('/* Net ' + self.model_name + ' - IOPT */\n'
                               '/* Automatic code generated by IOPT2C XSLT transformation. */\n'
                               '/* Changed by I2C4IOPT to run in Arduino */\n'
                               '/* Please fill the necessary code to perform hardware IO. */\n\n'
                               '#include <stdlib.h>\n#include "net_types.h"\n\n#include <Arduino.h>\n#define ANALOG_IN_MAX  1023\n'
                               '#define ANALOG_OUT_MAX 255\n\n//PYTHON - Initializations\n#include <Wire.h>\n')
            f_write.write('#define I2C_ADDRESS_ME ' + self.this_address + '\n' +
                                  self.get_init_addresses_string() +
                                  'String readString;\n' +
                                  self.get_events_flags_str() +
                                  '//PYTHON - End Initializations\n\n')

            f_write.write('//PYTHON - Receive Listener Function\n' +
                                  'void receiveI2C(int num) {\n' +
                                  self.TAB + 'readString = "";\n'+
                                  self.TAB + 'while (Wire.available() > 0) {\n' +
                                  self.TAB + self.TAB +  'delay(4);\n' +
                                  self.TAB + self.TAB + 'char c = Wire.read();\n' +
                                  self.TAB + self.TAB + 'readString += c;\n' + self.TAB + '}\n' +
                                  self.get_receive_string_verification() +
                                  '\n}\n//PYTHON - End Listener Function\n\n')

            f_write.write('/* Executed just once, before net execution starts: */\n' +
                          'void ' + self.model_name + '_InitializeIO()\n{\n')
            f_write.write(self.TAB + '//PYTHON - Initialize digital outputs\n')
            for k in range(len(self.DIGITAL_PORTS)):
                f_write.write(self.TAB + 'pinMode(' + str(self.DIGITAL_PORTS[k]) + ', OUTPUT);\n')
                f_write.write(self.TAB + 'digitalWrite(' + str(self.DIGITAL_PORTS[k]) + ', LOW);\n')
            f_write.write(self.TAB + '//PYTHON - Initialize serial and i2c communications\n' +
                                  self.TAB + 'Serial.begin(9600);\n' +
                                  self.TAB + 'Wire.begin(I2C_ADDRESS_ME);\n' +
                                  self.TAB + '//PYTHON - End serial and i2c initializations\n}\n\n')
            f_write.write(self.get_inputs_places_string())
            f_write.write(self.get_event_flag_check_string())
            f_write.write('}\n\n')
            f_write.write(self.get_output_places_string())
            f_write.write(self.get_send_comm_string())
            f_write.write('}\n\n')
            f_write.write('/* Delay between loop iterations to save CPU and power consumption */\n' +
                          'void ' + self.model_name + '_LoopDelay()\n{\n' +
                           self.TAB + '//PYTHON - Loop config\n' +
                           self.TAB + 'delay(10);\n' +
                           self.TAB + 'Serial.println("Loop ' + str(self.this_address) + '");\n' +
                           self.TAB + 'Wire.onReceive(receiveI2C);\n' +
                           self.TAB + '//PYTHON - End loop config\n}\n\n')
            f_write.write('/* Must return 1 to finish net execution */\n' +
                          'int ' + self.model_name + '_FinishExecution( ' + self.model_name + '_NetMarking* marking )\n' +
                         '{\n' + self.TAB + 'return 0;\n' + '}')
            print("DONE")
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except ValueError:
            print "Could not convert data to an integer."
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def get_init_addresses_string(self):
        string = ""
        for i in self.addresses:
            string += '#define I2C_ADDRESS_' + i['event'] + ' ' + i['address'] + '\n'
        return string



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
        string = self.TAB + 'if( events != NULL ) {\n'
        string += self.TAB + self.TAB + '// PYTHON - Change event state\n'
        for i in self.input_events:
            string += self.TAB + self.TAB + 'if (' + i + '_flag) {\n' +\
                      self.TAB + self.TAB + self.TAB + 'events->' + i + ' = 1;\n' +\
                      self.TAB + self.TAB + self.TAB + i + '_flag = 0;\n' +\
                      self.TAB + self.TAB + '} else {\n' +\
                      self.TAB + self.TAB + self.TAB + 'events->'+ i + ' = 0;\n' +\
                      self.TAB + self.TAB + '}\n'
        string += self.TAB + self.TAB + '//PYTHON - End change event state\n' + self.TAB + '}\n'
        return string

    def get_inputs_places_string(self):

        string = '/* Read all hardware input signals and fill data-structure */\n' +\
                 'void ' + self.model_name + '_GetInputSignals(\n' +\
                 self.TAB + self.model_name + '_InputSignals* inputs,\n' +\
                 self.TAB + self.model_name + '_InputSignalEvents* events )\n{\n'
        if len(self.inputs) == 0:
            string += self.TAB + '/* No Inputs*/\n\n'
        else:
            string += self.TAB + '//PYTHON - Digital read the inputs\n'
            for i, item in enumerate(self.inputs):
                string += self.TAB + 'inputs->' + item + ' = digitalRead(' + str(self.DIGITAL_PORTS[i]) + ');\n'
            string += self.TAB + '//PYTHON - End digital read the inputs\n'
        return string

    def get_output_places_string(self):
        string = '/* Write all output values to physical hardware outputs */\n' +\
                 'void ' + self.model_name + '_PutOutputSignals(\n' +\
                 self.TAB + self.model_name + '_PlaceOutputSignals* place_out,\n' +\
            self.TAB + self.model_name + '_EventOutputSignals* event_out,\n' +\
            self.TAB + self.model_name + '_OutputSignalEvents* events )\n{\n'
        if len(self.outputs) == 0:
            string += self.TAB + '/* No Outputs*/\n' + self.TAB + '\n\n'
        else:

            string += self.TAB + '//PYTHON - Digital write the outputs\n'
            for i, item in enumerate(self.outputs):
                string += self.TAB + 'digitalWrite(' + str(self.DIGITAL_PORTS[i + len(self.inputs)]) + ', place_out->' + item + ');\n'
            string += self.TAB + '//PYTHON - End digital write the outputs\n\n'
        return string

    def get_send_comm_string(self):
        string = self.TAB + 'if( events != NULL ) {\n'
        string += self.TAB + self.TAB + '//PYTHON - Send communication\n'
        for i in self.output_events:
            string += self.TAB + self.TAB + 'if (events->' + i+ ') {\n' +\
                      self.TAB + self.TAB + self.TAB + 'Wire.beginTransmission(I2C_ADDRESS_' + i + ');\n' + \
                      self.TAB + self.TAB + self.TAB + 'Wire.write("' + i + '");\n' + \
                      self.TAB + self.TAB + self.TAB + 'Wire.endTransmission();\n' + \
                      self.TAB + self.TAB + '}\n'
        string += self.TAB + self.TAB + '//PYTHON - End send communication\n' + self.TAB + '}\n\n'
        return string


    def ask_for_addresses(self):
        # This device address
        for k in self.output_events:
            for model in self.models:
                for e in model['events']:
                    if e == k:
                        self.addresses.append(
                            {
                                'address': model['address'],
                                'event'  : k
                            })
            #address = raw_input("Enter the address of " + k + " device: ")

        print 'Addresses'
        print self.addresses
        self.updateAddressesLabel()



    def get_file_data(self):
        '''
            Method to count the number of events in this net
            @param file_content content of the input file
            @return number of events in this net
        '''

        input_digital_string = re.findall(r'.InputSignalEvents(.*)input_fv != NULL.*', self.file_content, re.S)
        self.inputs = re.findall(r'inputs->(.*) = 0;', input_digital_string[0])
        print "\nInputs"
        for i, item in enumerate(self.inputs):
            print 'Digital ' + str(self.DIGITAL_PORTS[i]) + " -> " + item
        print len(self.inputs)

        #output events string
        output_events_string = re.findall(r'.OutputSignalEvents(.*)LoopDelay().*', self.file_content, re.S)
        self.outputs = re.findall(r'place_out->(.*) \*\/', output_events_string[0][0])
        print "\nOutputs: "
        for i, item in enumerate(self.outputs):
            print 'Digital ' + str(self.DIGITAL_PORTS[i + len(self.inputs)]) + " -> " + item
        print len(self.outputs)

        # input events string
        input_events_string = re.findall(r'.GetInputSignals\(.*events != NULL(.*)input_fv != NULL.*', self.file_content, re.S)
        print "\nInput Events: "
        if len(input_events_string) > 0:
            self.input_events = re.findall(r'events->(.*) \*\/', input_events_string[0])
        print self.input_events
        print len(self.input_events)

        print "\nOutput Events: "
        self.output_events = re.findall(r'events->(.*) \*\/', output_events_string[0][0])
        print self.output_events
        print len(self.output_events)

        self.model_name = re.findall(r'.starts: \*/\nvoid (.*)_InitializeIO().*', self.file_content, re.S)[0][0]


    def get_all_outputs(self):
        # return all inputs on this file
        f_read = open(self.input_file, 'r')
        input_events_string = re.findall(r'.GetInputSignals\(.*events != NULL(.*)input_fv != NULL.*', f_read.read(), re.S)
        inputs = re.findall(r'events->(.*) \*\/', input_events_string[0])
        f_read.close()
        return inputs




if __name__ == "__main__":
    app = NSApplication.sharedApplication()

    # Initiate the contrller with a XIB
    viewController = MainController.alloc().initWithWindowNibName_("Main")

    # Show the window
    viewController.showWindow_(viewController)

    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)

    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()