#############################################################################
# import packages
##############################################################################
import math
import os
from tkinter import *
from tkinter import ttk as ttk, Entry
from tkinter import filedialog


from pathfinding import SetupRoutes, config
from pathfinding.Utils import PrintRoutes

###################################################################################
# INPUT UI
###################################################################################
class MainUI:
    room_file_entry: Entry
    data_folder_entry: Entry
    robust_factor_spinbox: ttk.Spinbox
    num_of_agents_spinbox: ttk.Spinbox
    num_of_routes_spinbox: ttk.Spinbox
    num_of_routes_range_label: Label
    status_label: Label
    damage_steps_spinbox: Entry
    route_file_entry: Entry
    agentsEntries: []
    createRoutesFrame: ttk.LabelFrame
    include_step_num: IntVar

    def main(self):
        main_dialog = self.create_main_dialog()
        self.create_general_data_frame(main_dialog, 1)
        self.create_routes_frame(main_dialog, 2)
        self.create_print_route_frame(main_dialog, 3)
        self.create_MDR_frame(main_dialog, 4)

        ttk.Separator(main_dialog, orient=HORIZONTAL).grid(row=11, sticky=EW, columnspan=10)
        self.create_run_buttons(main_dialog, 12)

        # Status Bar
        self.status_label = Label(main_dialog, text="Ready", bd=1, relief=SUNKEN, anchor=W)
        self.status_label.grid(row=100, column=0, columnspan=20, sticky=EW)

        main_dialog.grid_rowconfigure(10, weight=1)
        mainloop()

    def create_main_dialog(self):
        main_dialog = Tk()
        w = 590
        h = 670

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
        self.room_file_entry = Entry(frame, width=65)
        self.room_file_entry.insert(0, config.room_file_default)
        #self.room_file_entry.insert(0, os.getcwd())

        self.room_file_entry.grid(row=0, column=2, sticky=W)
        ttk.Button(frame, text="Browse", command=self.browse_room_file).grid(row=0, column=3, sticky=E, padx=4)

        Label(frame, text="Data Folder:").grid(row=2, column=1, sticky=W)
        self.data_folder_entry = Entry(frame, width=65)
        self.data_folder_entry.insert(0, config.data_folder_default)
        #self.data_folder_entry.insert(0, os.getcwd())
        self.data_folder_entry.grid(row=2, column=2, sticky=W)
        ttk.Button(frame, text="Browse", command=self.browse_data_folder).grid(row=2, column=3, sticky=E, padx=4)

    def create_routes_frame(self, main_dialog, frame_row_index):
        self.createRoutesFrame = ttk.LabelFrame(main_dialog, text="Routes Data", padding=10)  # inside padding
        frame = self.createRoutesFrame
        frame.grid(row=frame_row_index, pady=10, padx=10, sticky=EW, columnspan=10)  # outside padding

        Label(frame, text="Number of Agents:").grid(row=0, column=0, sticky=W, pady=3, padx=3, columnspan=2)
        self.num_of_agents_spinbox = ttk.Spinbox(frame, from_=1, to=30, width=8, command=self.num_of_agents_updated)
        self.num_of_agents_spinbox.grid(row=0, column=2, sticky=W)
        self.num_of_agents_spinbox.delete(0, 'end')
        self.num_of_agents_spinbox.insert(0, config.num_of_agents_default)

        Label(frame, text="Number of Routes:").grid(row=2, column=0, sticky=W, pady=3, padx=3, columnspan=2)
        self.num_of_routes_spinbox = ttk.Spinbox(frame, from_=1, to=30, width=8)
        self.num_of_routes_spinbox.grid(row=2, column=2, sticky=W)
        self.num_of_routes_spinbox.delete(0, 'end')
        self.num_of_routes_spinbox.insert(0, config.num_of_routes_default)
        maxRoutes = math.factorial(config.num_of_agents_default)
        self.num_of_routes_spinbox.configure(to=maxRoutes)
        self.num_of_routes_range_label = Label(frame, text="(Min:1 Max:" + str(maxRoutes) + ")")
        self.num_of_routes_range_label.grid(row=2, column=3, sticky=W, pady=3, padx=3, columnspan=2)

        Label(frame, text="Robust Factor:").grid(row=1, column=0, sticky=W, pady=3, padx=3, columnspan=2)
        self.robust_factor_spinbox = ttk.Spinbox(frame, from_=1, to=30, width=8)
        self.robust_factor_spinbox.grid(row=1, column=2, sticky=W)
        self.robust_factor_spinbox.delete(0, 'end')
        self.robust_factor_spinbox.insert(0, config.robust_factor_default)

        # table header
        Label(frame, text="Must Reach\nTarget(%)").grid(row=4 , column=1)
        Label(frame, text="Motion\nEquation").grid(row=4 , column=2)
        Label(frame, text="Start Policy").grid(row=4, column=3)
        Label(frame, text="Goal Policy").grid(row=4, column=4)
        Label(frame, text="Adversarial").grid(row=4, column=5)
        Label(frame, text="D.S Budget").grid(row=4 , column=6)

        self.agentsEntries = []
        self.num_of_agents_updated()

    def create_print_route_frame(self, main_dialog, frame_row_index):
        frame = ttk.LabelFrame(main_dialog, text="Print Route", padding=10)  # inside padding
        frame.grid(row=frame_row_index, pady=10, padx=10, sticky=EW, columnspan=10)  # outside padding

        Label(frame, text="Route:").grid(row=0, column=0, sticky=W, pady=3, padx=3)
        self.route_file_entry = Entry(frame, width=65)
        self.route_file_entry.insert(0, config.route_file_default)
        self.route_file_entry.grid(row=0, column=1, sticky=W)
        ttk.Button(frame, text="Browse", command=self.browse_route_file).grid(row=0, column=2, sticky=E, padx=4)

        self.include_step_num = IntVar()
        Checkbutton(frame, text="Include Step No.", var=self.include_step_num).grid(row=1, column=0, columnspan=2, sticky=W)
        ttk.Button(frame, text="Print", command=self.print_routes).grid(row=1, column=2, sticky=E, padx=4)


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

    def browse_route_file(self):
        self.route_file_entry.delete(0, 'end')
        self.route_file_entry.insert(0, filedialog.askopenfilename())

    def create_routes(self):
        self.status_label.config(text='Running..')
        map_file_name = self.room_file_entry.get()
        data_folder = self.data_folder_entry.get()
        robust_factor = int(self.robust_factor_spinbox.get())
        num_of_agents = int(self.num_of_agents_spinbox.get())
        num_of_routes = int(self.num_of_routes_spinbox.get())
        SetupRoutes.create_routes(map_file_name, data_folder, robust_factor, num_of_agents, num_of_routes)
        self.status_label.config(text='Ready')

    def create_run_buttons(self, main_dialog, row_index):
        ttk.Button(main_dialog, text='Create Routes',   command=self.create_routes)         .grid(row=row_index, column=0, sticky=W, pady=4, padx=5)
        ttk.Button(main_dialog, text='Validate Routes',   command=self.not_implemented_yet) .grid(row=row_index, column=1, sticky=W, pady=4, padx=5)
        ttk.Button(main_dialog, text='Run MDR',         command=self.not_implemented_yet)   .grid(row=row_index+1, column=0, sticky=W, pady=4, padx=5)

    def num_of_agents_updated(self):
        newNumOfAgents = int(self.num_of_agents_spinbox.get())
        oldNumOfAgents = len(self.agentsEntries)

        # update maximum routes
        max_routes = math.factorial(newNumOfAgents)
        self.num_of_routes_spinbox.configure(to=max_routes)
        if int(self.num_of_routes_spinbox.get()) > max_routes:
            self.num_of_routes_spinbox.set(max_routes)
        self.num_of_routes_range_label.configure(text="(Min:1 Max:" + str(max_routes) + ")")

        if oldNumOfAgents < newNumOfAgents:
            #add new rows
            for i in range(oldNumOfAgents + 1, newNumOfAgents + 1):
                curr_row = i + 4
                cols = []

                # agent label
                agent_label = Label(self.createRoutesFrame, text="Agent " + str(i))
                agent_label.grid(row=curr_row, column=0, sticky=W)
                cols.append(agent_label)

                # Must reach target % - spinbox 0-100
                reach_target_spinbox = ttk.Spinbox(self.createRoutesFrame, from_=0, to=100, width=10)
                reach_target_spinbox.grid(row=curr_row, column=1, sticky=W)
                reach_target_spinbox.set(0)
                cols.append(reach_target_spinbox)

                # Motion Equation - combobox - 9/8/6/5
                motion_equation = ttk.Combobox(self.createRoutesFrame, values=["9", "8", "6", "5"], width=10)
                motion_equation.grid(row=curr_row, column=2)
                motion_equation.current(0)
                cols.append(motion_equation)
                #print(motion_equation.current(), motion_equation.get())

                # Start Policy - combobox - stay/ appear
                start_policy = ttk.Combobox(self.createRoutesFrame, values=["Stay", "Appear"], width=10)
                start_policy.grid(row=curr_row, column=3)
                start_policy.current(1)
                cols.append(start_policy)

                # Goal Policy - combobox - stay/ disappear
                goal_policy = ttk.Combobox(self.createRoutesFrame, values=["Stay", "Disappear"], width=10)
                goal_policy.grid(row=curr_row, column=4)
                goal_policy.current(1)
                cols.append(goal_policy)

                # Adversarial - combobox - Yes/No
                is_adversarial = ttk.Combobox(self.createRoutesFrame, values=["Yes", "No"], width=10)
                is_adversarial.grid(row=curr_row, column=5)
                is_adversarial.current(1)
                if i == 1:
                    is_adversarial.current(0)
                cols.append(is_adversarial)

                # D.S Budget - combobox - NA/1/2/3... Or Spinbox disabled/enabled
                d_s_budget = ttk.Combobox(self.createRoutesFrame, values=["NA", "1", "2", "3", "4", "5"], width=10)
                d_s_budget.grid(row=curr_row, column=6)
                d_s_budget.current(0)
                if i == 1:
                    d_s_budget.current(3)
                cols.append(d_s_budget)

                self.agentsEntries.append(cols)

        else:
            #remove rows
            for i in range(oldNumOfAgents, newNumOfAgents, -1):
                for e in self.agentsEntries[i-1]:
                    e.grid_remove()
                del self.agentsEntries[i-1]

    def print_routes(self):
        self.status_label.config(text='Running..')
        map_file = self.room_file_entry.get()
        route_file = self.route_file_entry.get()
        PrintRoutes.print_route(map_file, route_file, self.include_step_num.get())
        self.status_label.config(text='Ready')

    def not_implemented_yet(self):
        print ("Not Implemented Yet!")

if __name__ == "__main__":
    mainUI = MainUI()
    mainUI.main()