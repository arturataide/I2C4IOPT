
import tkinter
import tkinter.messagebox
from IOPT2AC_distributed import AddSerialToCode
import glob, zipfile, os, os.path, re

class MainView():
    def __init__(self):

        # init variables
        self.DIR = 'zip_files/'
        self.dirs = []
        # window
        # Create the main window widget.
        self.top_level_window = tkinter.Tk()
        self.top_level_window.title('IOPT2AC Tool')
        self.top_level_window.grid_rowconfigure(1, weight=1)
        self.top_level_window.grid_columnconfigure(0, weight=1)

        self.top_label = tkinter.Label(self.top_level_window, text='Copy all zip model files to "zip_files" folder')
        self.file_counter_label = tkinter.Label(self.top_level_window, text='<not counter yet>')
        self.file_counter_button = tkinter.Button(self.top_level_window, text='Verify models in path', command=self.count_files)
        self.generate_models_button = tkinter.Button(self.top_level_window, text='Generate Arduino Files', command=self.unzip_files)
        self.model_generated_label = tkinter.Label(self.top_level_window, text='<not generated yet>')
        self.addresses_label = tkinter.Label(self.top_level_window, text='<not generated yet>')
        self.events_label = tkinter.Label(self.top_level_window, text='<not generated yet>')
        # Call the Label widget's grid method.
        self.top_label.grid(row = 0, column = 0, sticky = 'nsew', pady = 10)
        self.file_counter_button.grid(row = 1, column = 0, sticky = 'nsew', pady = 10)
        self.file_counter_label.grid(row = 1, column = 1, sticky = 'nsew', pady = 10)
        self.generate_models_button.grid(row = 2, column = 0, sticky = 'nsew', pady = 10)
        self.model_generated_label.grid(row = 2, column = 1, sticky = 'nsew', pady = 10)
        self.addresses_label.grid(row = 3, column = 0, sticky = 'nsew', pady = 10)
        self.events_label.grid(row = 3, column = 1, sticky = 'nsew', pady = 10)



        # send self.top_level_window to front of all others (to be visible)
        # see also http://stackoverflow.com/questions/1892339/how-to-make-a-window-jump-to-the-front
        self.top_level_window.attributes('-topmost', True)

         # force a minimun size
        self.top_level_window.minsize(500, 50)


        self.count_files()
        # enter mainloop to really start the application. This thread blocks.
        tkinter.mainloop()
        #self.models = []

    def count_files(self):
        # count zip files in folder
        files = len(glob.glob(self.DIR + '*.zip'))
        models_number = "There are " + str(files) + " compressed models."
        self.file_counter_label.config(text=models_number)

    def unzip_files(self):
        self.addresses = []
        self.models = []
        self.dirs = []
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
        # remove unused files and rename main file
        self.removeUnusedFiles()
        self.prepareAddresses()
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
        names = ""
        events_str = ""
        for d in self.dirs:
            self.input_file = self.DIR + d + '/net_io.c'
            print("Preparing addresses in " + self.input_file)
            events = AddSerialToCode.get_all_inputs(self.input_file)
            events_str += str(events)
            name = d.split('/')[-1]
            model = {
                    'address': hex(len(self.models) + 1),
                    'model': name,
                    'events': events
            }
            names += model['model'] + " -> " + model['address'] + "\n"
            print("TESTE: " + str(model))
            self.models.append(model)
        self.events_label.config(text=events_str)
        self.addresses_label.config(text=names)
        print("Done")


    def write_IO_files(self):
        print("Writing files")
        i = 0
        for d in self.dirs:

            _input = self.DIR + d + '/net_io.c'
            _output = self.DIR + d + '/net_io.cpp'
            print(_input)
            print(_output)
            addSerialToCode = AddSerialToCode(_input, _output, self.models[i]['address'], self.models)
            print("to write")
            i += 1
            os.remove(_input)
            #self, input_file, output_file, address, models):
        print("Done, Ready to run in Arduino")
        self.model_generated_label.config(text="Models are ready to be burned in Arduino")

if __name__ == "__main__":
    main_view = MainView()
