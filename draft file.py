import pandas as pd
from scipy.signal import butter, filtfilt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
begin_process = time.time()
print(begin_process)
#Define functions
def butter_lowpass_filter(data):
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)


# Import data
wd = '/Volumes/WORK/imec-mict-ugent/Cyclop/'
df = pd.read_csv(wd + 'cyclop2.csv', sep=';')

# rearrange timestamp column to the end of the dataframe
df = df[[' eda', ' co2_0', ' rh_0', ' temp_0', ' co2_1', ' rh_1', ' temp_1', 'timestamp']]

# Create annotations dataframe
annotations_data = {
    'annotation': ['aan', 'binnen in bodybox', '2 min stilstaan', 'eerste oefening', 'stilstaan 1', 'tweede oefening',
                   'stilstaan 2', 'derde oefening', 'squat', 'stilstaan 3', 'einde'],
    'timestamp': ['1704711523', '1704711907', '1704711931', '1704712084', '1704712388', '1704712449', "1704712746",
                  '1704712799', '1704712812', '1704712842', '1704712927']}

df_annotations = pd.DataFrame(annotations_data, columns=['timestamp', 'annotation'])
df_annotations['timestamp'] = df_annotations['timestamp'].astype('int')
df_annotations['annotation'] = df_annotations['annotation'].astype('string')

# Calculate elapsed time in minutes
start_timestamp = df['timestamp'].iloc[0]
df['elapsed_time_minutes'] = (df['timestamp'] - start_timestamp) / 60

# Merge both datasets into one
df_out = pd.merge(df, df_annotations, how='left', on='timestamp')

#Add Alsico data
Alsico = pd.read_csv(wd + 'Alsico_data2.csv')
Alsico = pd.merge(Alsico, df_out, left_on='segment', right_on='annotation').drop_duplicates(subset= ['segment', 'timestamp', 'conditie']).reset_index(drop=True)

standards = ['2 min stilstaan', 'eerste oefening', 'stilstaan 1', 'tweede oefening', 'stilstaan 2', 'derde oefening',
             'stilstaan 3']
annotations = df_out[~df_out['annotation'].isin(standards)].drop_duplicates(subset = 'annotation').dropna(subset = 'annotation').reset_index(drop=True)
standards = df_out[df_out['annotation'].isin(standards)].drop_duplicates(subset= ['annotation', 'timestamp']).reset_index(drop=True)
headers = df_out.columns.values.astype('str')
del(df, df_annotations, annotations_data, start_timestamp, )

# Filter data and plot a figure
fig = make_subplots(rows=5, cols=2,subplot_titles=['EDA', 'RH_1','CO2_0', 'TEMP_1', 'RH_0', 'Geen Ventilatie', 'TEMP_0', 'Alsico Ventilatie', 'CO2_1' ])
fig.update_layout(height=1500, width=1600)
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'cyan', 'violet']
T = len(df_out['timestamp'].unique()) / 60
fs = 50.0
cutoff = 0.05
nyq = 0.5 * fs
order = 2

for i in range(7):
    row = i + 1 if i<5 else 1 if i == 5 else row +1
    col = 1 if i < 5 else 2
    yf = butter_lowpass_filter(df_out.iloc[:, i])
    fig.add_trace(go.Scatter(y=df_out.iloc[:, i],
                             x=df_out['elapsed_time_minutes'],
                             line=dict(shape='spline'),
                             name=f'{df_out.columns[i]} Raw'),
                  row= row, col= col)
    fig.add_trace(go.Scatter(y=yf, x=df_out['elapsed_time_minutes'], line=dict(shape='spline'), name=f'{df_out.columns[i]} Filt.'),
                  row=row, col=col)
    for ii in range(len(standards)):
        fillcolor = colors[ii] if ii < 7 else colors[ii]
        fig.add_vrect(type='rect', x0=standards['elapsed_time_minutes'][ii],
                      x1=standards['elapsed_time_minutes'][ii + 1] if ii < 6 else annotations['elapsed_time_minutes'].max(),
                      row=row, col=col, fillcolor=fillcolor, line_width=0, opacity=.20)
    for iii in range(len(annotations)):
        fig.add_vline(x=annotations['elapsed_time_minutes'][iii], line_width=1, line_dash="dash",
                      annotation_text=annotations['annotation'][iii])

# Plot Alsico data
for conditie in ['ventilatie', 'geen ventilatie']:
    for particle_size in ['particles <= 5', 'particles >= 0.5']:
        fig.add_trace(go.Scatter(y=Alsico[particle_size][Alsico['conditie'] == conditie],
                                 x=Alsico['elapsed_time_minutes'][Alsico['conditie'] == conditie],
                                 name=f'{particle_size}, {conditie}', line_shape="hv"),
                      row=3 if conditie == 'ventilatie' else 4, col=2)
    for ii in range(len(standards)):
        fillcolor = colors[ii] if ii < 7 else colors[ii]
        fig.add_vrect(type='rect', x0=standards['elapsed_time_minutes'][ii],
                      x1=standards['elapsed_time_minutes'][ii + 1] if ii < 6 else annotations['elapsed_time_minutes'].max(),
                      row=3 if conditie == 'ventilatie' else 4, col=2, fillcolor=fillcolor, line_width=0, opacity=.20)
    for iii in range(len(annotations)):
        fig.add_vline(x=annotations['elapsed_time_minutes'][iii], line_width=1, line_dash="dash",
                      annotation_text=annotations['annotation'][iii])

fig.update_xaxes(range=[0,df_out['elapsed_time_minutes'].max()])


# Save HTML file
fig.write_html(wd + "file.html")

end_process = time.time()
print(end_process - begin_process)