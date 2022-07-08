import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


def separate_number_chars(s):
    res = re.split('([-+]?\d+\.\d+)|([-+]?\d+)', s.strip())
    res_f = [r.strip() for r in res if r is not None and r.strip() != '']
    first = res_f[0]
    return first


def get_initials(string):
    if string != '':
        lista = list(string)
        n = ''
        n += string[0]
        for e, i in enumerate(lista):
            if i == ' ':
                n += lista[e+1]
        return n

'''
# panel score and people's score don't correlate too much (0.34)
corr_scores = df['PanelScore'].corr(df['ComScore'])
# removing the tequilas with few votes (< 10, roughly half) raises it to 0.54
df2 = df.drop(df[df['N_Ratings'] < 10].index, inplace=False)
corr_scores_thresh = df2['PanelScore'].corr(df2['ComScore'])

# print the unique contents of the string variables, to get a feel of variability in them
# df_obj.nunique()

# histogram of N tequilas by category
plt.figure(figsize=(15, 10))
df.groupby("Category").size().sort_values(ascending=False).plot.bar()
plt.xticks(rotation=80)
plt.xlabel("Tequila category")
plt.ylabel("Number of bottles in the data")
plt.show

# show distributions over unique entries of variables in part of dash
# also put bubble plots by category [Blanco, Anejo, Extra Anejo, Reposado]

'''
app = dash.Dash()

df = pd.read_csv('C:\\Users\\sadek\\OneDrive\\Documenti\\GitHub\\Tequiloco\\Tequilas_TQMM.csv')
# remove trailing white spaces from variable names
df.columns = df.columns.str.strip()
# select variables that contain strings
df_obj = df.select_dtypes(['object'])
# remove trailing white spaces from those too
df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
# remove weird things from alcohol
df['ABV/Proof'] = df['ABV/Proof'].apply(lambda x: separate_number_chars(x))
# rename NOM to Distillery and take out "Previously ..."
df.rename(columns={'NOM': 'Distillery'}, inplace=True)
df['Distillery'] = df['Distillery'].apply(lambda x: separate_number_chars(x))
# Do something about variables with too long contents ("Fermentation")
# remove 100% agave (almost all have it)
df["Fermentation"] = df["Fermentation"].map(lambda x: x.lstrip('100% agave'))
# take only initials of strings
df["Fermentation"] = df["Fermentation"].map(lambda x: get_initials(x))
df["Aging"] = df["Aging"].map(lambda x: get_initials(x))

variables_to_plot = ['Agave Type', 'Agave Region', 'Aging', 'ABV/Proof', 'Cooking', 'Distillery', 'Distillation', 'Extraction','Fermentation', 'Still',  'Water Source']
categories_to_plot = ['Blanco', 'Añejo', 'Extra Añejo', 'Reposado']

for v in variables_to_plot:
    df.loc[df[v] == '-', v] = 'None'

app.layout = html.Div(id='parent', children=[
    html.H1(id='H1', children='Choose tequila category and feature to plot', style={'textAlign': 'center',
                                                                                    'marginTop': 40, 'marginBottom': 40}),
    dcc.Dropdown(
            id="Category",
            options=[{"label": x, "value": x} for x in categories_to_plot],
            value="Blanco",
        ),
    dcc.Dropdown(
            id="Variable",
            options=[{"label": x, "value": x} for x in variables_to_plot],
            value="Agave Type",
        ),
    dcc.Graph(id='scatter_plot')])


@app.callback(Output(component_id='scatter_plot', component_property='figure'),
              [Input("Category", "value"), Input("Variable", "value")])
def graph_update(dd1, dd2):
    summary_df = pd.DataFrame()
    summary_df['Avg Rating'] = df.loc[df['Category'] == dd1].groupby(dd2).mean()['PanelScore']
    summary_df['Number of tequila bottles in data'] = df.loc[df['Category'] == dd1].groupby(dd2)['Name'].count()
    summary_df['Types'] = summary_df.index

    fig = px.scatter(data_frame=summary_df, x='Types', y='Avg Rating',
                     size='Number of tequila bottles in data',
                     hover_data={'Avg Rating': True, 'Number of tequila bottles in data': True, 'Types': False},
                     color=summary_df.index, size_max=summary_df['Number of tequila bottles in data'].max()/2)

    fig.update_layout(title=dd1 + ' tequilas: Expert rating by ' + dd2,
                      xaxis_title='Types',
                      yaxis_title='Ratings'
                      )
    return fig


app.run_server()



'''
# make this into a dashboard
for cat in categories_to_plot:
    for x in variables_to_plot:
        tiny_df = pd.DataFrame()
        tiny_df['Avg Rating'] = df.loc[df['Category'] == cat].groupby(x).mean()[y]
        tiny_df['Sample Size'] = df.loc[df['Category'] == cat].groupby(x)['Name'].count()

        plt.figure(figsize=(15, 10))
        p = sns.scatterplot(data=tiny_df, x=tiny_df.index, y='Avg Rating', size="Sample Size", hue=tiny_df.index, legend=False, sizes=(20, 2000))
        p.set_xlabel('')
        p.set_title(cat + ' tequilas: Expert rating by ' + x)
        plt.xticks(rotation=80)
        plt.show()

# to run decision tree with tastes as well,
# normalize taste features (from Agave cooked), remove sparse ones

# give avg alcohol content of category to missing ones

# weight N ratings? as a sales proxy measure
'''