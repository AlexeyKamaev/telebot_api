import sys
import os

import pandas as pd
import numpy as np
import pickle

import geopy.distance as dis
from funcions.entities import Preprocessor, Model

from sklearn import set_config
set_config(transform_output="pandas")

filename_pipe = './funcions/data/model_ltl.pkl'

metro_path = './funcions/data/metro_model.pkl'

weights_path = './funcions/data/model.pkl'

y_mean = 18_500_000


def dist(c1,c2):
    return dis.geodesic(c1, c2).km

def dist_maker_df(df: pd.DataFrame, Y):
    dists = {'kremlin_dist': (55.752004, 37.617734),
             'moskva_city_dist': (55.749776, 37.536234)}
    
    for place, coord in dists.items():
        df[place] = [dist(c1, coord) for c1 in Y]


def Result_Maker(json):
    set_config(transform_output="pandas")

    metro = pd.read_pickle(metro_path)
    ml_pipeline = pickle.load(open(filename_pipe, 'rb'))

    X = pd.DataFrame(json, index=[0])
    X = X.rename(columns={'square':'total_area','quality':'repair_type','lat':'latitude','lan':'longitude'})

    X[['total_area','latitude','longitude']] = X[['total_area','latitude','longitude']].astype(float)
    Y = tuple(zip(X['latitude'].astype(float), X['longitude'].astype(float)))

    dist_maker_df(X,Y)

    metro['dist'] = [dist(c, Y) for c in metro.coords]
    metro_m = metro[metro['dist'] == min(metro['dist'])].iloc[0,3]
    X['metro_m'] = metro_m    
    
    X_pred = ml_pipeline.predict(X)

    
    result = int(np.round(X_pred,-4)[0])

    return result, metro_m


def Result_Maker_MAX(data):

    set_config(transform_output="pandas")
    
    data = data.dict()

    df = pd.DataFrame([data])
    pr = Preprocessor(df)
    pr.transform()
    data = pr.to_pandas()


    model = Model(data)

    pred = model.load_predict(
        data,
        weights=weights_path)
    

    
    result = int(np.round(pred,-4)[0])

    return result