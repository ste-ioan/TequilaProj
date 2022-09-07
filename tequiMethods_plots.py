import xgboost as xg
import pandas as pd
from matplotlib import pyplot
import numpy as np
import plotly.express as px
from scipy.stats import sem

df = pd.read_csv('C:\\Users\\sadek\\OneDrive\\Documenti\\GitHub\\TequiLoco\\preProc_tequilaData.csv')
pd.options.mode.chained_assignment = None

# barplots of fermentation and aging methods barplots
# misleading to lump them all together so do the ones that are actually comparable (e.g. with vs with out ferm)

# fermentation plots
# creating the dataset
data1 = {'With fibers': df.loc[df['with_fibers_ferm'] == 1, 'PanelScore'].mean(),
         'Without fibers': df.loc[df['without_fibers_ferm'] == 1, 'PanelScore'].mean()}
conds = list(data1.keys())
vals = list(data1.values())
serrs = list([sem(df.loc[df['with_fibers_ferm'] == 1, 'PanelScore']),
              sem(df.loc[df['without_fibers_ferm'] == 1, 'PanelScore'])])

fig = pyplot.figure(figsize=(10, 5))

# creating the bar plot
pyplot.bar(conds, vals, color=(0.1, 0.1, 0.1, 0.1), edgecolor='maroon', width=0.4, yerr=serrs)
pyplot.ylim([80, 95])
pyplot.xlabel("Fiber fermentation")
pyplot.ylabel("Expert rating")
pyplot.title('All tequilas: fiber fermentation')
pyplot.show()

# open air, wood, cement, stainless steel
data2 = {'Stainless': df.loc[df['Stainless_steel_tanks_ferm'] == 1, 'PanelScore'].mean(),
         'Open air': df.loc[df['Open-air_ferm'] == 1, 'PanelScore'].mean(),
         'Wood': df.loc[df['Wood_ferm'] == 1, 'PanelScore'].mean(),
         'Cement': df.loc[df['Cement_ferm'] == 1, 'PanelScore'].mean()}
conds = list(data2.keys())
vals = list(data2.values())
serrs = list([sem(df.loc[df['Stainless_steel_tanks_ferm'] == 1, 'PanelScore']),
              sem(df.loc[df['Open-air_ferm'] == 1, 'PanelScore']),
              sem(df.loc[df['Wood_ferm'] == 1, 'PanelScore']),
              sem(df.loc[df['Cement_ferm'] == 1, 'PanelScore'])])

# creating the bar plot
pyplot.bar(conds, vals, color=(0.1, 0.1, 0.1, 0.1), edgecolor='maroon', width=0.4, yerr=serrs)
pyplot.ylim([80, 95])
pyplot.xlabel("Fermentation tanks type")
pyplot.ylabel("Expert rating")
pyplot.title('All tequilas: fermentation tanks')
pyplot.show()

# AGING
data3 = {'American White Oak': df.loc[df['American_White_Oak_age'] == 1, 'PanelScore'].mean(),
         'French Oak': df.loc[df['French_Oak_age'] == 1, 'PanelScore'].mean(),
         'Hungarian Oak': df.loc[df['Hungarian_Oak_age'] == 1, 'PanelScore'].mean(),
         }
conds = list(data3.keys())
vals = list(data3.values())
serrs = list([sem(df.loc[df['American_White_Oak_age'] == 1, 'PanelScore']),
              sem(df.loc[df['French_Oak_age'] == 1, 'PanelScore']),
              sem(df.loc[df['Hungarian_Oak_age'] == 1, 'PanelScore'])])

fig = pyplot.figure(figsize=(10, 5))

# creating the bar plot
pyplot.bar(conds, vals, color=(0.1, 0.1, 0.1, 0.1), edgecolor='maroon', width=0.4, yerr=serrs)
pyplot.ylim([80, 95])
pyplot.xlabel("Oak types")
pyplot.ylabel("Expert rating")
pyplot.title('All tequilas: Oak barrel type')
pyplot.show()

data4 = {'Used barrels': df.loc[df['Used_barrels_age'] == 1, 'PanelScore'].mean(),
         'New barrels': df.loc[df['New_barrels_age'] == 1, 'PanelScore'].mean(),
         }
conds = list(data4.keys())
vals = list(data4.values())
serrs = list([sem(df.loc[df['Used_barrels_age'] == 1, 'PanelScore']),
              sem(df.loc[df['New_barrels_age'] == 1, 'PanelScore'])])

fig = pyplot.figure(figsize=(10, 5))

# creating the bar plot
pyplot.bar(conds, vals, color=(0.1, 0.1, 0.1, 0.1), edgecolor='maroon', width=0.4, yerr=serrs)
pyplot.ylim([80, 95])
pyplot.xlabel("Use types")
pyplot.ylabel("Expert rating")
pyplot.title('All tequilas: Used or new barrel type')
pyplot.show()

data5 = {'Cognac': df.loc[df['Cognac_casks_age'] == 1, 'PanelScore'].mean(),
         'Sherry': df.loc[df['Sherry_casks_age'] == 1, 'PanelScore'].mean(),
         'Wine': df.loc[df['Wine_casks_age'] == 1, 'PanelScore'].mean(),
         'Port': df.loc[df['Port_casks_age'] == 1, 'PanelScore'].mean(),
         'Bourbon': df.loc[df['Bourbon_barrels_age'] == 1, 'PanelScore'].mean(),
         'Whisky': df.loc[df['Whisky_barrels_age'] == 1, 'PanelScore'].mean(),
         'Rum': df.loc[df['Rum_barrels_age'] == 1, 'PanelScore'].mean(),
         'Scotch': df.loc[df['Scotch_barrels_age'] == 1, 'PanelScore'].mean(),
         }
conds = list(data5.keys())
vals = list(data5.values())
serrs = list([sem(df.loc[df['Cognac_casks_age'] == 1, 'PanelScore']),
              sem(df.loc[df['Sherry_casks_age'] == 1, 'PanelScore']),
              sem(df.loc[df['Wine_casks_age'] == 1, 'PanelScore']),
              sem(df.loc[df['Port_casks_age'] == 1, 'PanelScore']),
              sem(df.loc[df['Bourbon_barrels_age'] == 1, 'PanelScore']),
              sem(df.loc[df['Whisky_barrels_age'] == 1, 'PanelScore']),
              sem(df.loc[df['Rum_barrels_age'] == 1, 'PanelScore']),
              sem(df.loc[df['Scotch_barrels_age'] == 1, 'PanelScore']),
              ])

fig = pyplot.figure(figsize=(10, 5))

# creating the bar plot
pyplot.bar(conds, vals, color=(0.1, 0.1, 0.1, 0.1), edgecolor='maroon', width=0.4, yerr=serrs)
pyplot.ylim([80, 95])
pyplot.xlabel("Casks type")
pyplot.ylabel("Expert rating")
pyplot.title('All tequilas: Other distilled casks')
pyplot.show()
