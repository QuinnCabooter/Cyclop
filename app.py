from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
wd = '/Volumes/WORK/imec-mict-ugent/Cyclop/'

#get data
df = pd.read_csv(wd + 'df_out.csv')

#Get figure
fig = px.line(df, y=" co2_0", x="elapsed_time_minutes")


#Initialize app
app = Dash(__name__)

#App layout
app.layout = html.Div([html.H1(children='Raw data from Sensorbox'), dcc.Graph(id = "plot", figure=fig),  dash_table.DataTable(data=df.to_dict('records'))])
#run the app
if __name__ == '__main__':
    app.run(debug = True)