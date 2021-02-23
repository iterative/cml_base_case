import geopandas as gpd
import cartopy.crs as ccrs
from cartopy import feature as cfeature
import glob
import matplotlib.pyplot as plt
import pandas as pd
from pandas.api.types import is_numeric_dtype
import os

from get_dataset import merge_ibge_data
from utils.helpers import get_parent_dirs


if '__main__' == __name__:
    LOCAL_DIR = os.getcwd()
    
else:
    LOCAL_DIR = os.path.dirname(str(__file__))

FIGURES_DIRECTORY = os.path.join(get_parent_dirs(1) , r'results\figure')

if not os.path.exists(FIGURES_DIRECTORY):
    os.makedirs(FIGURES_DIRECTORY)


OCEAN = cfeature.OCEAN
LAND = cfeature.LAND

def check_if_numeric(x):

    try:
        return is_numeric_dtype(x)
        
    except:
        return False

def make_fig_and_axes(fig_name):
    
    projection = ccrs.PlateCarree()
    
    fig, ax = plt.subplots(subplot_kw={'projection':projection})
    
    fig.suptitle(fig_name)
    
    ax.coastlines(resolution='50m', color='black', linewidth=1)
    ax.add_feature(OCEAN, zorder=0)
    ax.add_feature(LAND, zorder=0, edgecolor='black')
    
    gl = ax.gridlines(draw_labels=True)
    gl.top_labels=False
    gl.right_labels=False
    
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
    