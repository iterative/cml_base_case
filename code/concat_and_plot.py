import geopandas as gpd
import glob
import matplotlib.pyplot as plt
import pandas as pd
from pandas.api.types import is_numeric_dtype
import os
import numpy as np
import yaml
from get_dataset import merge_ibge_data
from utils.helpers import get_parent_dirs



FIGURES_DIRECTORY = os.path.join(r'results\figure')

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
    
    gl = ax.grid()
    
    fig_filename = os.path.join(FIGURES_DIRECTORY, fig_name + '.png')
    
    print('saving {1} in \n\t {0} \n\n'.format(FIGURES_DIRECTORY, (fig_name + '.png')))
    
    return fig, ax, fig_filename

def write_to_yaml(dict_of_filenames):

    
    print(dict_of_filenames)
    
    yaml_filename = os.path.join(get_parent_dirs(1),
                                 '.github', 'workflows',
                                 'list_of_plots.yaml')
    with open(yaml_filename, 'w') as file:
        documents = yaml.dump(dict_of_filenames, file)

def plot_datasets():

    gdf = merge_ibge_data().to_crs(epsg= 4326)
    
    dict_of_filenames = {'filenames': dict()}
    
    i = 0
    
    for col in gdf.columns:
        if check_if_numeric(gdf[col]):
            i = i + 1
            if i >5:
                break
            print('Plotting figure of {0}'.format(col), end='\n'*3)
        
            fig, ax, fig_filename = make_fig_and_axes(col)
        
            gdf.plot(column=col, ax=ax)
            
            fig.show()
            
            fig.savefig(fig_filename,dpi=100)
            
            dict_of_filenames['filenames'][col] = '/'.join(str(fig_filename).split('cml_base_case')[1:])
            
            plt.close(fig)
    
    
    write_to_yaml(dict_of_filenames)
    
if '__main__' == __name__:
    plot_datasets()
    
