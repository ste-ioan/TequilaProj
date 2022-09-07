import xgboost as xg
import pandas as pd
from matplotlib import pyplot
import numpy as np
import plotly.express as px
from scipy.stats import sem
from sklearn.inspection import PartialDependenceDisplay
import shap

df = pd.read_csv('C:\\Users\\sadek\\OneDrive\\Documenti\\GitHub\\TequiLoco\\preProc_tequilaData.csv')
pd.options.mode.chained_assignment = None

for cat in ['Blanco', 'Reposado', 'Joven', 'Añejo', 'Extra Añejo']:
    sub_df = df.loc[df['Category'] == cat, :]

    # drop tequilas w no taste features for this df
    clean_sub_df = sub_df.loc[sub_df.loc[:, 'Agave (cooked)':'Chlorine'].isna().all(axis=1) == 0, :]
    # replace nans with 0s in both
    sub_df = sub_df.fillna(0)
    clean_sub_df = clean_sub_df.fillna(0)

    y = sub_df['PanelScore']
    X = sub_df.loc[:, 'ABV/Proof':]

    # deploy the model on each tequila category
    model = xg.XGBRegressor()
    model.fit(X, y)
    # stash the importance of features outside of the xgboost codes
    importance = model.get_booster().get_score(importance_type='weight', fmap='')
    tuples = [(k, importance[k]) for k in importance]
    N_feats_above_mean = (model.feature_importances_ > model.feature_importances_.mean()).sum()
    tuples = sorted(tuples, key=lambda x: x[1])[-N_feats_above_mean:]
    feats, _ = zip(*tuples)

    # plot importance scores with xgboost native
    xg.plot_importance(model, title=cat + ' tequila importance scores of ' + str(N_feats_above_mean) + ' out of '
                                    + str(len(df.columns)) + ' features', max_num_features=N_feats_above_mean,
                       ylabel='taste features')
    # pyplot.show()
    # pyplot.savefig('C:\\Users\\sadek\\PycharmProjects\\wineScraper\\data\\tequilas\\' + cat + ' feat_importance.png')
    # pyplot.close()

    # partial dependence plots could be useful with the features identified above, to assess impact on rating
    # in the meantime just bubble plot of feature value by rating scores may be interesting to look at

    # any feat containing '_' in its name
    binary_feats = list(filter(lambda x: '_' in x, sub_df.columns))
    '''
    for feat in feats:

        # if it's a binary feat, use full dataset, otherwise use the cleaned one
        if feat in binary_feats:
            sub_df2 = sub_df
        else:
            sub_df2 = clean_sub_df

        summary_df = pd.DataFrame()
        summary_df['N Bottles'] = pd.concat([sub_df2.loc[sub_df2[feat] != 0, :].groupby('PanelScore').count().mean(axis=1), sub_df2.loc[sub_df2[feat] == 0, :].groupby('PanelScore').count().mean(axis=1)])
        summary_df['Feat Val'] = pd.concat([sub_df2.loc[sub_df2[feat] != 0, ['PanelScore', feat]].groupby('PanelScore').mean(), sub_df2.loc[sub_df2[feat] == 0, ['PanelScore', feat]].groupby('PanelScore').mean()])
        summary_df.reset_index(inplace=True)

        fig = px.scatter(data_frame=summary_df, x='Feat Val', y='PanelScore', size='N Bottles',
                         color='PanelScore', color_continuous_scale='turbo', size_max=80)
        fig.update_layout(title=cat + ' tequilas: Expert ratings by their ' + feat + ' feature average')
        fig.show()
    '''

    # above plots not very useful, learn about partial dependence plots...
    # [you can prolly remove fermentation and aging methods, thx to barplots]
    for feat in feats[-15:]:
        if feat not in binary_feats:
            shap.plots.partial_dependence(feat, model.predict, X.sample(100), ice=False, model_expected_value=True,
                                          feature_expected_value=True)
