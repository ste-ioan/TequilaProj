import pandas as pd
import re
import numpy as np


def separate_number_chars(s):
    if s != '-':
        res = re.split('([-+]?\d+\.\d+)|([-+]?\d+)', s.strip())
        res_f = [r.strip() for r in res if r is not None and r.strip() != '']
        res_f_dig = float(res_f[0])
    else:
        res_f_dig = np.nan
    return res_f_dig


df = pd.read_csv('C:\\Users\\sadek\\OneDrive\\Documenti\\GitHub\\Tequiloco\\Tequilas_TQMM.csv')
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

fermentation_methods_encoders = ['Stainless steel tanks', 'Open-air', 'with fibers', 'without fibers', 'Wood', 'Cement',
                                 'Champagne', 'Classical music']

for ferm in fermentation_methods_encoders:
    ferm_no_spaces = ferm.replace(' ', '_')
    df[ferm_no_spaces] = df.loc[:, 'Fermentation'].str.contains(ferm).astype(float)
    df.rename(columns={ferm_no_spaces: ferm_no_spaces + '_ferm'}, inplace=True)

aging_encoders = ['American White Oak', 'French Oak', 'Hungarian Oak', 'Used barrels', 'New barrels', 'Cognac casks',
                  'Sherry casks', 'Wine casks', 'Beer casks', 'Port casks', 'Bourbon barrels', 'Whisky barrels',
                  'Rum barrels', 'Scotch barrels']

for age in aging_encoders:
    age_no_spaces = age.replace(' ', '_')
    df[age_no_spaces] = df.loc[:, 'Aging'].str.contains(age).astype(float)
    df.rename(columns={age_no_spaces: age_no_spaces + '_age'}, inplace=True)

''' ALL THIS ELEGANT CODE WAS USELESS, AS 1-HOT ENCODING FOR CAT VARIABLES, COZ MODEL ASSUMES NUMERICAL RELATIONSHIP

category_aging_encoders = {'barrels': ['Whisky', 'Bourbon', 'Rum', 'Scotch'], 'casks': ['Cognac',
                                                                                        'Sherry', 'Wine', 'Port',
                                                                                        'Beer']}
for aging_ca in category_aging_encoders:
    col_name = aging_ca.capitalize()+'_aging'
    df[col_name] = ''
    for subcat in category_aging_encoders[aging_ca]:
        df.loc[df.loc[:, 'Aging'].str.contains(subcat), col_name] = df.loc[df.loc[:, 'Aging'].str.contains(subcat),
                                                                           col_name] + subcat

# let's convert those strings to numbers
le_csk = preprocessing.LabelEncoder()
le_csk.fit(df['Barrels_aging'].unique())
df['Barrels_aging'] = le_csk.transform(df['Barrels_aging'])
'''

# give average alcohol content to cells with missing alcohol
df.loc[df['ABV/Proof'].isna(), 'ABV/Proof'] = df['ABV/Proof'].mean()

# min-max normalize features {MAY NOT BE NECESSARY ??? will skip Y, ABV} n ready to go to trees
# X - Xmin
df.loc[:, 'Agave (cooked)':'Chlorine'] = df.loc[:, 'Agave (cooked)':'Chlorine'].subtract(
    df.loc[:, 'Agave (cooked)':'Chlorine'].min(axis=1), axis=0)
# outcome of above divided by Xmax-Xmin
df.loc[:, 'Agave (cooked)':'Chlorine'] = df.loc[:, 'Agave (cooked)':'Chlorine'].divide(df.loc[:, 'Agave (cooked)':
                                                                                                 'Chlorine'].max(
    axis=1).subtract(df.loc[:, 'Agave (cooked)':'Chlorine'].min(axis=1)), axis=0)

# fill nan, but first drop any tequila with all NANs in the taste features
# moved to other code, since a lot of data got thrown out like this
# df = df.loc[df.loc[:, 'Agave (cooked)':'Chlorine'].isna().all(axis=1) == 0, :]
# df = df.fillna(0)

feats_to_drop = ['Name', 'Distillery', 'Agave Type', 'Agave Region', 'Region', 'Cooking', 'Extraction', 'Water Source',
                 'Fermentation', 'Still', 'Aging', 'Other', 'N_Ratings', 'ComScore', 'Distillation']

df.drop(feats_to_drop, axis=1, inplace=True)
# let's swap ABV and PanelScore
a = df.columns.tolist()
index = df.columns.get_loc("PanelScore")
a.pop(index)
a.insert(1, "PanelScore")
df = df[a]

df.to_csv('C:\\Users\\sadek\\OneDrive\\Documenti\\GitHub\\TequiLoco\\preProc_tequilaData.csv')
