import os
import tkinter as tk
import time
from tkinter import ttk, messagebox
import pandas as pd

#TODO: Make sure that the timestamps from the sensorbox match the timestamps from the annotations
#TODO: Check if it works in spyder


# Create dataframe to save annotation data
df = {"Participant_ID": [], "Protocol": [], "timestamp": [], "annotation": []}

# Function to check if participant ID already exists
def participant_exists(participant_id):
    folder_path = "Experiment_data"
    for filename in os.listdir(folder_path):
        if filename.startswith(f"PP_{participant_id}_annotations"):
            return True
    return False

#TODO: Add other input fields
# Function to get user input
def get_user_input():
    root = tk.Tk()
    root.title("Experiment Input")

    tk.Label(root, text="Participant ID:").grid(row=0, column=0)
    participant_id_entry = tk.Entry(root)
    participant_id_entry.grid(row=0, column=1)

    tk.Label(root, text="Select Protocol:").grid(row=1, column=0)
    protocol_var = tk.StringVar(root)
    protocol_var.set("Standaard_protocol")  # default value
    protocol_menu = ttk.Combobox(root, textvariable=protocol_var)
    protocol_menu['values'] = list(protocols.keys())
    protocol_menu.grid(row=1, column=1)

    def on_submit():
        try:
            participant_id = int(participant_id_entry.get())
            if participant_exists(participant_id):
                messagebox.showerror("Duplicate ID", "Participant ID already exists.")
                return
            selected_protocol = protocol_var.get()
            root.quit()
            return participant_id, selected_protocol
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid integer for Participant ID.")

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.grid(row=2, columnspan=2)

    root.mainloop()

    participant_id = participant_id_entry.get()
    selected_protocol = protocol_var.get()
    root.destroy()

    return int(participant_id), selected_protocol

if __name__ == "__main__":
    # Get user input
    participant_id, selected_protocol = get_user_input()

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
        df["Participant_ID"].append(participant_id)
        df["Protocol"].append(selected_protocol)
        time.sleep(times[i])
        print("next segment")

    print("Experiment has ended.")

    # Save the data to a CSV file
    pd.options.display.float_format = '{:.0f}'.format
    df2 = pd.DataFrame.from_dict(df)
    df2.to_csv(f'Experiment_data/PP_{participant_id}_annotations.csv')