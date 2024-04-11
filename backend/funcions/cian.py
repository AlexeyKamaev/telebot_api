import pandas as pd
import pickle

from funcions.entities import Preprocessor, Model
from funcions.Parser import Parser

from sklearn import set_config

data_path    = './funcions/data/90000_base.pkl'
weights_path = './funcions/data/model.pkl'
filename_pipe = './funcions/data/model_ltl.pkl'
base_path = './funcions/data/cian_base.pkl'


def load_base():
    df = pd.read_pickle(base_path)
    return df

def findr(id):

    set_config(transform_output="pandas")

    id = int(id)

    json = {'total_area':-1,'repair_type':'No data','lat':-1,'lan':-1,'metro_dist':-1,'metro':'-1','kremlin_dist':-1,'pred':-1,'real':-1, 'link': 'No data'}
    link = f'cian.ru/sale/flat/{id}'

    try:
        url = [f'https://www.cian.ru/sale/flat/{id}']
        z = {}
        pr = Parser()
        x = pr.get_data(urls=url)[0]
        
        for k,v in x.items():
            z[k] = [v]

        X = pd.DataFrame.from_dict(z)

        preproc = Preprocessor(path_or_DF=X)

        preproc.transform()

        X = preproc.to_pandas()

        x = Model(X).model(weights_path).predict(X)

        json = {'total_area':float(X.total_area),'repair_type':str(X.repair_type),'lat':float(X.latitude),'lan':float(X.longitude),'metro_dist':float(X.metro_dist),'metro':str(X.metro_m),'kremlin_dist':float(X.kremlin_dist),'pred':x,'real':float(X.price), 'link': str(link)}
        return json
        
    except:
        try:

            df = load_base()
            f = df.index == id

            total_area = df.loc[f].iloc[:,4].item()
            repair_type = df.loc[f].iloc[:,7].item()
            lat = df.loc[f].iloc[:,10].item()
            lan = df.loc[f].iloc[:,11].item()
            
            metro_dist = df.loc[f].iloc[:,18].item()
            kremlin_dist = df.loc[f].iloc[:,21].item()
            pred = df.loc[f].iloc[:,27].item()
            real = df.loc[f].iloc[:,28].item()
            metro = df.loc[f].iloc[:,3].item()
            json = {'total_area':float(total_area),'repair_type':str(repair_type),'lat':float(lat),'lan':float(lan),'metro_dist':float(metro_dist),'metro':str(metro),'kremlin_dist':float(kremlin_dist),'pred':float(pred),'real':float(real), 'link': str(link)}

            return json
        except:
            return json
        