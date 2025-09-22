"""
Author: Quinn Cabooter
Date: 14-01-2025
Last updated: 20-01-2025

Python script that returns a '.csv' file with te annotations and corresponding timestamps of an 
experiment. The user can input the participant ID, session number, protocol, ventilation enabled, 
company, location, room, garment type, inner garment type and wash cycles. 
The script will then run the experiment based on the selected protocol.

"""

# Import necessary libraries
import os
import tkinter as tk
import time
import threading
import pandas as pd

# Import necessary libraries for GUI
from tkinter import ttk, messagebox

# Import custom protocols
from customVariables import protocols, garments, inner_garments, fabric_types, goggle_types

timestamp = int(time.time())
#timestamp = int(time.time()-3600)


# Define data folder path
DATA_FOLDER_PATH = "Experiment_data"

# Create data folder if it does not exist
if not os.path.exists("Experiment_data"):
    os.makedirs("Experiment_data")

# Create dataframe to save annotation data
df = {
    "participantID": [], "sessionNumber": [], "protocol": [], "timestamp": [], "annotation": [],
    "ventilationEnabled": [], "company": [], "location": [], "room": [], "garmentType": [], 
    "innerGarmentType": [], "fabricType":[], "goggleType": [], "washCycles": []
    }

## Create functions for the script
# Function to check if participant ID already exists
def participant_exists(participant_id: int, session_number: int) -> bool:
    for filename in os.listdir(DATA_FOLDER_PATH):
        if filename.startswith(f"Participant_{participant_id}_Session_{session_number}"):
            return True
    return False

# Function to make sure that the input is an integer and not strings in for example participant number.
def validate_integer(P):
    return P.isdigit() or P == ""

# Function to capture manual annotations
def capture_manual_annotations():
    global experiment_running
    while experiment_running:
        manual_annotation = input("Enter manual annotation here:\n")
        if manual_annotation.lower() == 'exit':
            experiment_running = False
            break
        current_time = int(time.time()-3600)
        append_annotation_data(current_time, manual_annotation)
        print(f"Manual annotation added at {int(current_time)}: {manual_annotation}\n")

# Function to append annotation data to the dataframe
def append_annotation_data(timestamp: int, annotation: str):
    df["timestamp"].append(timestamp)
    df["annotation"].append(annotation)
    df["participantID"].append(participant_id)
    df["sessionNumber"].append(session_number)
    df["protocol"].append(selected_protocol)
    df["ventilationEnabled"].append(ventilation_enabled)
    df["company"].append(company)
    df["location"].append(location)
    df["room"].append(room)
    df["garmentType"].append(garment_type)
    df["innerGarmentType"].append(inner_garment_type)
    df["washCycles"].append(wash_cycles)
    df["fabricType"].append(fabric_type)
    df["goggleType"].append(goggle_type)

# Function to get user input
def get_user_input():
    root = tk.Tk()
    root.title("Experiment Input")
        
    # Validate command for the entry fields
    vcmd = (root.register(validate_integer), '%P')

    ## Fields with text input
    # Participant ID
    tk.Label(root, text="Participant ID:").grid(row=0, column=0)
    participant_id_entry = tk.Entry(root)
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


    ## Fields with dropdown menu
    # Protocol
    tk.Label(root, text="Select Protocol:").grid(row= 6, column=0)
    protocol_var = tk.StringVar(root)
    protocol_var.set(list(protocols.keys())[0])  # default value, first protocol
    protocol_menu = ttk.Combobox(root, textvariable=protocol_var)
    protocol_menu['values'] = list(protocols.keys())
    protocol_menu.grid(row=6, column=1)
    # Garment type
    tk.Label(root, text="Select Garment:").grid(row= 7, column=0)
    garment_var = tk.StringVar(root)
    garment_var.set(garments[0])  # default value
    garment_menu = ttk.Combobox(root, textvariable=garment_var)
    garment_menu['values'] = garments
    garment_menu.grid(row=7, column=1)
    # Inner garment type
    tk.Label(root, text="Select Inner Garment:").grid(row= 8, column=0)
    inner_garment_var = tk.StringVar(root)
    inner_garment_var.set(inner_garments[0])  # default value
    inner_garment_menu = ttk.Combobox(root, textvariable=inner_garment_var)
    inner_garment_menu['values'] = inner_garments
    inner_garment_menu.grid(row=8, column=1)
    # Fabric type
    tk.Label(root, text="Select Fabric:").grid(row= 9, column=0)
    fabric_var = tk.StringVar(root)
    fabric_var.set(fabric_types[0])  # default value  # default value
    fabric_menu = ttk.Combobox(root, textvariable=fabric_var)
    fabric_menu['values'] = fabric_types
    fabric_menu.grid(row=9, column=1)
    # Goggle type
    tk.Label(root, text="Select Goggle:").grid(row= 10, column=0)
    goggle_var = tk.StringVar(root)
    goggle_var.set(goggle_types[0])  # default value
    goggle_menu = ttk.Combobox(root, textvariable=goggle_var)
    goggle_menu['values'] = goggle_types
    goggle_menu.grid(row=10, column=1)

    ## Fields with check boxes
    # Ventilation enabled
    tk.Label(root, text="Ventilation enabled:").grid(row= 11, column=0)
    ventilation_var = tk.BooleanVar(root, value=False)
    ventilation_checkbox = tk.Checkbutton(root, variable=ventilation_var)
    ventilation_checkbox.grid(row=11, column=1)

    # Add a label to the GUI
    label = tk.Label(root, text="!!! CHECK PARTICIPANT NUMBER, SESSION NUMBER AND VENTILATION !!!")
    label.grid(row=12, column=0, pady = 20, columnspan=2)

    def on_submit():
        try:
            participant_id = int(participant_id_entry.get())
            session_number = session_number_entry.get()
            if participant_exists(participant_id, session_number):
                messagebox.showerror(
                    "Duplicate ID", 
                    "This participant ID and session number combination already exists.")
                return
            selected_protocol = protocol_var.get()
            ventilation_enabled = ventilation_var.get()
            company = company_var.get()
            location = location_var.get()
            room = room_var.get()
            garment_type = garment_var.get()
            inner_garment_type = inner_garment_var.get()
            fabric_type = fabric_var.get()
            goggle_type = goggle_var.get()
            wash_cycles = wash_cycles_var.get()

            root.quit()
            return (participant_id, selected_protocol, session_number, ventilation_enabled, 
                    company, location, room, garment_type, inner_garment_type, wash_cycles, 
                    fabric_type, goggle_type)
        except ValueError:
            messagebox.showerror(
                "Invalid input", 
                "Please enter a valid integer for Participant ID.")

    submit_button = tk.Button(root, text="Start experiment", command=on_submit)
    submit_button.grid(row=13, columnspan=2, pady=10)

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
    fabric_type = fabric_var.get()
    goggle_type = goggle_var.get()

    root.destroy()

    return (int(participant_id), selected_protocol, int(session_number), ventilation_enabled, 
            company, location, room, garment_type, inner_garment_type, wash_cycles, 
            fabric_type, goggle_type)

# Shared flag for experiment running state
experiment_running = True

if __name__ == "__main__":
    # Get user input
    (participant_id, selected_protocol, session_number, ventilation_enabled, company, 
     location, room, garment_type, inner_garment_type, wash_cycles, 
     fabric_type, goggle_type) = get_user_input()

    # Determine the annotations and times based on the selected protocol
    annotations = protocols[selected_protocol]["annotations"]
    times = protocols[selected_protocol]["times"]

    # Print the start time of the experiment
    print("\n!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Experiment is running...")
    print("!!!!!!!!!!!!!!!!!!!!!!!!\n")

    start_time = int(timestamp)
    print(f"Experiment started at: {start_time}\n")

    # Start manual annotation thread
    manual_thread = threading.Thread(target=capture_manual_annotations, daemon=True)
    manual_thread.start()

    # Run the experiment
    for i in range(len(annotations)):
        current_time = int(timestamp)
        append_annotation_data(current_time, annotations[i])
        time.sleep(times[i])
        print(f"Automatic annotation added at {current_time}: {annotations[i]}\n")
        print("Enter manual annotation here:\n")

    # Save the data to a CSV file
    pd.options.display.float_format = '{:.0f}'.format
    df2 = pd.DataFrame.from_dict(df)
    df2.to_csv(
        f"{DATA_FOLDER_PATH}/Participant_{participant_id}_Session_{session_number}" +
        f"_annotations_{start_time}.csv", 
        index=False
    )

    # Send a message to the user that the experiment has ended
    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("THE EXPERIMENT HAS ENDED, TYPE 'exit' TO CLOSE THE PROGRAM")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    experiment_running = False  # Stop the manual annotation thread
    manual_thread.join()


