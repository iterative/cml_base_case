import geopandas as gpd
import pandas as pd
import glob
import os
from utils.helpers import get_parent_dirs

def get_ibge_relacional(filename='PA_2018.shp'):

    dir_path = os.path.join(
    
                'data/ibge/shp_relacional'
                )
                
    filename = os.path.join(dir_path, filename)
    
    gdf = gpd.read_file(filename)
    
    gdf['COD_MUNIC7'] = gdf['CD_GEOCMU'].apply(lambda x: str(int(x))[:7])
    
    df = pd.DataFrame(gdf).drop(columns=['CD_GEOCMU', 'geometry'])
    
    return df



def get_ibge_census_data(filename='Domi_Entorno_normalized_formatados.csv'):

    dir_path = os.path.join( 
    
                'data/ibge/censo'
                )
                
    filename = os.path.join(dir_path, filename)
    df = pd.read_csv(filename)
    
    df['CD_GEOCODI'] = df['Cod_setor'].apply(lambda x: str(int(x)))
    
    df = df.drop(columns=['Cod_setor'])
    
    df['COD_MUNIC7'] = df['CD_GEOCODI'].apply(lambda x: str(x)[:7])
    
    return df

def get_census_tract_shp_data(filename='15SEE250GC_SIR.shp'):
    
    dir_path = os.path.join( 
    
                'data/ibge/shp_censo'
                )
                
    filename = os.path.join(dir_path, filename)
    
    gdf = gpd.read_file(filename)
    
    gdf['CD_GEOCODI'] = gdf['CD_GEOCODI'].astype(str)
    
    return gdf

def merge_ibge_data():
    censo = get_ibge_census_data()
    df = get_ibge_relacional()
    census_tract = get_census_tract_shp_data()
    
    to_concat = [censo, df]
    result = census_tract.copy()
    
    for df, keys in zip(to_concat, ['CD_GEOCODI', 'COD_MUNIC7']):
        result = result.merge(df, on=keys, how='left').fillna(0)
    
    return result

if '__main__' == __name__:

    gdf = merge_ibge_data()
    
