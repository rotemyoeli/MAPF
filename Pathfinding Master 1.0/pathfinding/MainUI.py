#############################################################################
# import packages
##############################################################################
from tkinter import *
from tkinter import ttk as ttk, Entry
from tkinter import filedialog

from pathfinding import SetupRoutes, config, ConvertToCSV


###################################################################################
# INPUT UI
###################################################################################
from pathfinding.Utils import PrintRoutes


class MainUI:
    room_file_entry: Entry
    data_folder_entry: Entry
    robust_factor_spinbox: ttk.Spinbox
    num_of_agents_spinbox: ttk.Spinbox
    num_of_routes_spinbox: ttk.Spinbox
    status_label: Label
    damage_steps_spinbox: Entry
    room_file_entry: Entry
    data_folder_entry: Entry
    agentsEntries: []
    createRoutesFrame: ttk.LabelFrame

    def main(self):
        main_dialog = self.create_main_dialog()
        self.create_general_data_frame(main_dialog, 1)
        self.create_routes_frame(main_dialog, 2)
        self.create_MDR_frame(main_dialog, 3)

        ttk.Separator(main_dialog, orient=HORIZONTAL).grid(row=11, sticky=EW, columnspan=10)
        self.create_run_buttons(main_dialog, 12)

        # Status Bar
        self.status_label = Label(main_dialog, text="Ready", bd=1, relief=SUNKEN, anchor=W)
        self.status_label.grid(row=100, column=0, columnspan=10, sticky=EW)

        main_dialog.grid_rowconfigure(10, weight=1)
        mainloop()

    def create_main_dialog(self):
        main_dialog = Tk()
        w = 560
        h = 500

        # get screen width and height
        ws = main_dialog.winfo_screenwidth()  # width of the screen
        hs = main_dialog.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        main_dialog.geometry('%dx%d+%d+%d' % (w, h, x, y))
        main_dialog.positionfrom()
        main_dialog.iconbitmap()  # TODO
        main_dialog.minsize(w, h)
        main_dialog.title("Multi Agent Path Finding 1.0")

        return main_dialog

    def create_general_data_frame(self, main_dialog, frame_row_index):
        frame = ttk.LabelFrame(main_dialog, text="General Data", padding=10)  # inside padding
        frame.grid(row=frame_row_index, pady=10, padx=10, sticky=EW, columnspan=10)  # outside padding

        Label(frame, text="Room:").grid(row=0, column=1, sticky=W)
        self.room_file_entry = Entry(frame, width=60)
        self.room_file_entry.insert(0, config.room_file_default)
        self.room_file_entry.grid(row=0, column=2, sticky=W)
        ttk.Button(frame, text="Browse", command=self.browse_room_file).grid(row=0, column=3, sticky=E, padx=4)

        Label(frame, text="Data Folder:").grid(row=2, column=1, sticky=W)
        self.data_folder_entry = Entry(frame, width=60)
        self.data_folder_entry.insert(0, config.data_folder_default)
        self.data_folder_entry.grid(row=2, column=2, sticky=W)
        ttk.Button(frame, text="Browse", command=self.browse_data_folder).grid(row=2, column=3, sticky=E, padx=4)

    def create_routes_frame(self, main_dialog, frame_row_index):
        self.createRoutesFrame = ttk.LabelFrame(main_dialog, text="Routes Data", padding=10)  # inside padding
        frame = self.createRoutesFrame
        frame.grid(row=frame_row_index, pady=10, padx=10, sticky=EW, columnspan=10)  # outside padding

        Label(frame, text="Number of Routes:").grid(row=0, column=0, sticky=W, pady=3, padx=3, columnspan=2)
        self.num_of_routes_spinbox = ttk.Spinbox(frame, from_=1, to=30, width=10)
        self.num_of_routes_spinbox.grid(row=0, column=2, sticky=W)
        self.num_of_routes_spinbox.delete(0, 'end')
        self.num_of_routes_spinbox.insert(0, config.num_of_routes_default)

        Label(frame, text="Robust Factor:").grid(row=1, column=0, sticky=W, pady=3, padx=3, columnspan=2)
        self.robust_factor_spinbox = ttk.Spinbox(frame, from_=1, to=30, width=10)
        self.robust_factor_spinbox.grid(row=1, column=2, sticky=W)
        self.robust_factor_spinbox.delete(0, 'end')
        self.robust_factor_spinbox.insert(0, config.robust_factor_default)

        Label(frame, text="Number of Agents:").grid(row=2, column=0, sticky=W, pady=3, padx=3, columnspan=2)
        self.num_of_agents_spinbox = ttk.Spinbox(frame, from_=1, to=30, width=10, command=self.num_of_agents_updated)
        self.num_of_agents_spinbox.grid(row=2, column=2, sticky=W)
        self.num_of_agents_spinbox.delete(0, 'end')
        self.num_of_agents_spinbox.insert(0, config.num_of_agents_default)

        # table header
        Label(frame, text="Val1").grid(row=4 , column=1, sticky=W)
        Label(frame, text="Val2").grid(row=4 , column=2, sticky=W)
        Label(frame, text="Val3").grid(row=4 , column=3, sticky=W)

        self.agentsEntries = []
        for i in range(1, config.num_of_agents_default+1):
            cols = []
            for j in range(4):
                if j == 0:
                    e = Label(frame, text="Agent " + str(i))
                    e.grid(row=i + 4, column=j, sticky=W)
                else:
                    e = Entry(frame, relief=RIDGE, width=15)
                    e.insert(END, i)
                    e.grid(row=i + 4, column=j, sticky=E)

                cols.append(e)
            self.agentsEntries.append(cols)

    def create_MDR_frame(self, main_dialog, frame_row_index):
        frame = ttk.LabelFrame(main_dialog, text="MDR Data", padding=10)  # inside padding
        frame.grid(row=frame_row_index, pady=10, padx=10, sticky=EW, columnspan=10)  # outside padding

        Label(frame, text="Damage Steps Budget:").grid(row=0, column=1, sticky=W)
        self.damage_steps_spinbox = ttk.Spinbox(frame, from_=1, to=30, width=10)
        self.damage_steps_spinbox.grid(row=0, column=2, sticky=W)
        self.damage_steps_spinbox.delete(0, 'end')
        self.damage_steps_spinbox.insert(0, config.damage_steps_default)

    def browse_room_file(self):
        self.room_file_entry.delete(0, 'end')
        self.room_file_entry.insert(0, filedialog.askopenfilename())

    def browse_data_folder(self):
        self.data_folder_entry.delete(0, 'end')
        self.data_folder_entry.insert(0, filedialog.askdirectory())

    def create_routes(self):
        self.status_label.config(text='Running..')

        map_file_name = self.room_file_entry.get()
        data_folder = self.data_folder_entry.get()
        robust_factor = int(self.robust_factor_spinbox.get())
        num_of_agents = int(self.num_of_agents_spinbox.get())
        SetupRoutes.create_routes(map_file_name, data_folder, robust_factor, num_of_agents)
        self.status_label.config(text='Ready')


    def create_run_buttons(self, main_dialog, row_index):
        ttk.Button(main_dialog, text='Create Routes',   command=self.create_routes)         .grid(row=row_index, column=0, sticky=E, pady=4, padx=5)
        ttk.Button(main_dialog, text='Print Routes',    command=self.print_routes)          .grid(row=row_index, column=1, sticky=E, pady=4, padx=5)
        ttk.Button(main_dialog, text='Convert to CSV1', command=self.convert_csv_step1)     .grid(row=row_index, column=2, sticky=E, pady=4, padx=5)
        ttk.Button(main_dialog, text='Convert to CSV2', command=self.convert_csv_step2)     .grid(row=row_index, column=3, sticky=E, pady=4, padx=5)
        ttk.Button(main_dialog, text='Run MDR',         command=self.not_implemented_yet)   .grid(row=row_index, column=4, sticky=E, pady=4, padx=5)

    def num_of_agents_updated(self):
        newNumOfAgents = int(self.num_of_agents_spinbox.get())
        oldNumOfAgents = len(self.agentsEntries)
        print("blabla new:" + str(newNumOfAgents) +" old:" + str(oldNumOfAgents))

        if oldNumOfAgents < newNumOfAgents:
            #add new rows
            for i in range(oldNumOfAgents+1, newNumOfAgents + 1):
                cols = []
                for j in range(4):
                    if j == 0:
                        e = Label(self.createRoutesFrame, text="Agent " + str(i))
                        e.grid(row=i + 4, column=j, sticky=W)
                    else:
                        e = Entry(self.createRoutesFrame, relief=RIDGE, width=15)
                        e.insert(END, i)
                        e.grid(row=i + 4, column=j, sticky=E)
                    cols.append(e)
                self.agentsEntries.append(cols)

        else:
            #remove rows
            for i in range(oldNumOfAgents, newNumOfAgents, -1):
                for j in range(4):
                    self.agentsEntries[i-1][j].grid_remove()
                del self.agentsEntries[i-1]

    def convert_csv_step1(self):
        self.status_label.config(text='Running..')
        data_folder = self.data_folder_entry.get()
        ConvertToCSV.step_one(data_folder)
        self.status_label.config(text='Ready')

    def convert_csv_step2(self):
        self.status_label.config(text='Running..')
        data_folder = self.data_folder_entry.get()
        ConvertToCSV.step_two(data_folder)
        self.status_label.config(text='Ready')

    def print_routes(self):
        self.status_label.config(text='Running..')
        data_folder = self.data_folder_entry.get()
        map_file = self.room_file_entry.get()
        route_file = "TODO"
        PrintRoutes.print_route(map_file, route_file)
        self.status_label.config(text='Ready')

    def not_implemented_yet(self):
        print ("Not Implemented Yet!")

if __name__ == "__main__":
    mainUI = MainUI()
    mainUI.main()