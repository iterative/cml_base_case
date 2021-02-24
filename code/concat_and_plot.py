import geopandas as gpd
import glob
import matplotlib.pyplot as plt
import pandas as pd
from pandas.api.types import is_numeric_dtype
import os

from get_dataset import merge_ibge_data
from utils.helpers import get_parent_dirs



FIGURES_DIRECTORY = os.path.join('results/figure')

if not os.path.exists(FIGURES_DIRECTORY):
    os.makedirs(FIGURES_DIRECTORY)

def check_if_numeric(x):

    try:
        return is_numeric_dtype(x)
        
    except:
        return False

def make_fig_and_axes(fig_name):

    fig, ax = plt.subplots(subplot_kw={'aspect':'equal'})
    
    fig.suptitle(fig_name)
    
    ax.coastlines(resolution='50m', color='black', linewidth=1)
    
    
    gl = ax.grids()
    
    fig_filename = os.path.join(FIGURES_DIRECTORY, fig_name + '.png')
    
    print('saving {1} in \n\t {0} \n\n'.format(FIGURES_DIRECTORY, (fig_name + '.png')))
    
    return fig, ax, fig_filename

def plot_datasets():

    gdf = merge_ibge_data().to_crs(epsg= 4326)
    
    for col in gdf.columns:
        if check_if_numeric(gdf[col]):
            print('Plotting figure of {0}'.format(col), end='\n'*3)
        
            fig, ax, fig_filename = make_fig_and_axes(col)
        
            gdf.plot(column=col, ax=ax)
            
            fig.show()
            
            fig.savefig(fig_filename)
            
            plt.close(fig)
    
    
if '__main__' == __name__:
    plot_datasets()
    
