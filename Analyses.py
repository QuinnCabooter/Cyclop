import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

annotation = pd.read_csv('/Users/Quinn/Library/CloudStorage/OneDrive-UGent/A. PhD/Alsico/' \
                            'Participant_7_Session_10_annotations_1758259490.csv')

annotation['timestamp'] = annotation['timestamp'] 
#annotation['timestamp'] = annotation['timestamp'] + 3600


sensordata = pd.read_csv('/Users/Quinn/Library/CloudStorage/OneDrive-UGent/A. PhD/Alsico/' \
                        'sensordata_1758263202.csv', sep=';')  

sensordata[' Timestamp_ms'] = sensordata[' Timestamp_ms'] / 1000

plt.plot(sensordata[' Timestamp_ms'], sensordata[' GSR'])
plt.xlabel('Time')
plt.ylabel('GSR')
plt.title('GSR over Time')
plt.show()

# Check data types and first few rows
print(sensordata.dtypes)
print(sensordata.head())

# Plot each column in sensordata
for column in sensordata.columns:
    if column != ' Timestamp_ms':  # Skip timestamp column for y-axis
        plt.figure(figsize=(10, 6))
        plt.plot(sensordata[' Timestamp_ms'], sensordata[column])
        plt.xlabel('Time')
        plt.ylabel(column.strip())  # Remove leading/trailing spaces
        plt.title(f'{column.strip()} over Time')
        plt.show()