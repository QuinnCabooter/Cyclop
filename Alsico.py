"""
Author: Quinn Cabooter
Date: 14-01-2025
Last updated: 15-01-2025

Python script that returns a '.csv' file with te annotations and corresponding timestamps of an experiment. The user can input the participant ID, session number, protocol, ventilation enabled, company, location, room, garment type, inner garment type and wash cycles. The script will then run the experiment based on the selected protocol.

"""


import os
import tkinter as tk
import time
from tkinter import ttk, messagebox
import pandas as pd

#import custom protocols
from customVariables import protocols, garments, inner_garments


#TODO: Make sure that the timestamps from the sensorbox match the timestamps from the annotations

# Create dataframe to save annotation data
df = {"participantID": [], "sessionNumber": [], "protocol": [], "timestamp": [], "annotation": [], "ventilationEnabled": [], "company": [], "location": [], "room": [], "garmentType": [], "innerGarmentType": [], "washCycles": []}

# Function to check if participant ID already exists
def participant_exists(participant_id, session_number):
    folder_path = "Experiment_data"
    for filename in os.listdir(folder_path):
        if filename.startswith(f"Participant_{participant_id}_Session_{session_number}"):
            return True
    return False

#TODO: Add other input fields
# Function to get user input
def get_user_input():
    root = tk.Tk()
    root.title("Experiment Input")

    # Function to make sure that the input is an integer and not strings in for example participant number.
    def validate_integer(P):
        if P.isdigit() or P == "":
            return True
        else:
            return False
        
    #Validate command for the entry fields
    vcmd = (root.register(validate_integer), '%P')

    ##Fields with text input
    # Participant ID
    tk.Label(root, text="Participant ID:").grid(row=0, column=0)
    participant_id_entry = tk.Entry(root, validate="key", validatecommand=vcmd)
    participant_id_entry.grid(row=0, column=1)
    # Session number
    tk.Label(root, text="Session Number:").grid(row=1, column=0)
    session_number_entry = tk.Entry(root, validate="key", validatecommand=vcmd)
    session_number_entry.grid(row=1, column=1)
    # Company
    tk.Label(root, text="Company:").grid(row=2, column=0)
    company_var = tk.Entry(root)
    company_var.grid(row=2, column=1)
    # Location
    tk.Label(root, text="Location:").grid(row=3, column=0)
    location_var = tk.Entry(root)
    location_var.grid(row=3, column=1)
    # Room
    tk.Label(root, text="Room:").grid(row=4, column=0)
    room_var = tk.Entry(root)
    room_var.grid(row=4, column=1)
    # Wash cycles
    tk.Label(root, text="Wash cycles:").grid(row=5, column=0)
    wash_cycles_var = tk.Entry(root, validate="key", validatecommand=vcmd)
    wash_cycles_var.grid(row=5, column=1)


    ##Fields with dropdown menu
    #Protocol
    tk.Label(root, text="Select Protocol:").grid(row= 6, column=0)
    protocol_var = tk.StringVar(root)
    protocol_var.set("Supersnel_protocol")  # default value, supersnel protocol
    protocol_menu = ttk.Combobox(root, textvariable=protocol_var)
    protocol_menu['values'] = list(protocols.keys())
    protocol_menu.grid(row=6, column=1)
    #Garment type
    tk.Label(root, text="Select Garment:").grid(row= 7, column=0)
    garment_var = tk.StringVar(root)
    garment_var.set("Garment1")  # default value
    garment_menu = ttk.Combobox(root, textvariable=garment_var)
    garment_menu['values'] = garments
    garment_menu.grid(row=7, column=1)
    #Inner garment type
    tk.Label(root, text="Select Inner Garment:").grid(row= 8, column=0)
    inner_garment_var = tk.StringVar(root)
    inner_garment_var.set("InnerGarment1")  # default value
    inner_garment_menu = ttk.Combobox(root, textvariable=inner_garment_var)
    inner_garment_menu['values'] = inner_garments
    inner_garment_menu.grid(row=8, column=1)

    ##Fields with check boxes
    tk.Label(root, text="Ventilation enabled:").grid(row= 9, column=0)
    ventilation_var = tk.BooleanVar(root, value=False)
    ventilation_checkbox = tk.Checkbutton(root, variable=ventilation_var)
    ventilation_checkbox.grid(row=9, column=1)

    # Add a label to the GUI
    label = tk.Label(root, text="!!! CHECK PARTICIPANT NUMBER, SESSION NUMBER AND VENTILATION !!!")
    label.grid(row=10, column=0, pady = 20, columnspan=2)

    def on_submit():
        try:
            participant_id = int(participant_id_entry.get())
            session_number = session_number_entry.get()
            if participant_exists(participant_id, session_number):
                messagebox.showerror("Duplicate ID", "This participant ID and session number combination already exists.")
                return
            selected_protocol = protocol_var.get()
            ventilation_enabled = ventilation_var.get()
            company = company_var.get()
            location = location_var.get()
            room = room_var.get()
            garment_type = garment_var.get()
            inner_garment_type = inner_garment_var.get()
            wash_cycles = wash_cycles_var.get()

            root.quit()
            return participant_id, selected_protocol, session_number, ventilation_enabled, company, location, room, garment_type, inner_garment_type, wash_cycles
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid integer for Participant ID.")

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.grid(row=11, columnspan=2)

    root.mainloop()

    participant_id = participant_id_entry.get()
    selected_protocol = protocol_var.get()
    session_number = session_number_entry.get()
    ventilation_enabled = ventilation_var.get()
    company = company_var.get()
    location = location_var.get()
    room = room_var.get()
    garment_type = garment_var.get()
    inner_garment_type = inner_garment_var.get()
    wash_cycles = wash_cycles_var.get()

    root.destroy()

    return int(participant_id), selected_protocol, int(session_number), ventilation_enabled, company, location, room, garment_type, inner_garment_type, wash_cycles

if __name__ == "__main__":
    # Get user input
    participant_id, selected_protocol, session_number, ventilation_enabled, company, location, room, garment_type, inner_garment_type, wash_cycles = get_user_input()

    # Determine the annotations and times based on the selected protocol
    annotations = protocols[selected_protocol]["annotations"]
    times = protocols[selected_protocol]["times"]

    # Print the start time of the experiment
    print("Experiment is running...")
    start_time = time.time()
    print("GMT")
    print(start_time)

    #TODO: Add code to save the other input fields
    # Run the experiment
    for i in range(len(annotations)):
        current_time = time.time()
        df["timestamp"].append(current_time)
        df["annotation"].append(annotations[i])
        df["participantID"].append(participant_id)
        df["sessionNumber"].append(session_number)
        df["protocol"].append(selected_protocol)
        df["ventilationEnabled"].append(False)
        df["company"].append(company)
        df["location"].append(location)
        df["room"].append(room)
        df["garmentType"].append(garment_type)
        df["innerGarmentType"].append(inner_garment_type)
        df["washCycles"].append(wash_cycles)

        time.sleep(times[i])
        print("next segment")

    print("Experiment has ended.")

    # Save the data to a CSV file
    pd.options.display.float_format = '{:.0f}'.format
    df2 = pd.DataFrame.from_dict(df)
    df2.to_csv(f'Experiment_data/Participant_{participant_id}_Session_{session_number}_annotations.csv')