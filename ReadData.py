import pandas as pd

# Define the path to the CSV file
csv_file_path = '/Users/Quinn/Documents/Cyclop/Experiment_data/PP_2_annotations.csv'

# Read the CSV file into a pandas DataFrame without adding an extra index column
df = pd.read_csv(csv_file_path, index_col=0)

# Print the DataFrame
print(df)