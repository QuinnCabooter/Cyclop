
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

annotation = pd.read_csv('/Users/Quinn/Library/CloudStorage/OneDrive-UGent/A. PhD/Alsico/' \
                            'Participant_7_Session_14_annotations_1758889306.csv')

annotation['timestamp'] = annotation['timestamp']
#annotation['timestamp'] = annotation['timestamp'] + 3600


sensordata = pd.read_csv('/Users/Quinn/Library/CloudStorage/OneDrive-UGent/A. PhD/Alsico/' \
                        'sensordata_1758889406.csv', sep=';')

sensordata[' Timestamp_ms'] = sensordata[' Timestamp_ms'] / 1000

# Plot each column in sensordata
for column in sensordata.columns:
    if column != ' Timestamp_ms':  # Skip timestamp column for y-axis
        plt.figure(figsize=(10, 6))
        plt.plot(sensordata[' Timestamp_ms'], sensordata[column])
        #plt.xlim(1000, 1100)  # Set x-axis limits to 0-50
        plt.xlabel('Time')
        plt.ylabel(column.strip())  # Remove leading/trailing spaces
        plt.title(f'{column.strip()} over Time')
        plt.show()