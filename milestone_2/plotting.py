import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd

def plot_pie(vals, labels, ax, title, with_labels=False):
    my_circle=plt.Circle( (0,0), 0.7, color='white')

    def func(pct, allvals):
        absolute = int(pct/20.*np.sum(allvals))
        return "{:.1f}%".format(pct,absolute)
    
    if with_labels:
        ax.pie(vals, labels=labels, autopct=lambda pct: func(pct, vals), radius=2);
    else:
        ax.pie(vals, autopct=lambda pct: func(pct, vals), radius=2);
    ax.add_artist(my_circle)
    ax.set_title(title, y=1.4)
    
    
def add_zero_values(df, elem_mapping, item_mapping):
    new_df = []
    for i in df.itemcode.unique():
        for e in df.elementcode.unique():
            data = df[(df.elementcode == e) & (df.itemcode == i)]
            if len(data) == 0:
                line = pd.Series({'elementcode': e, 'element': elem_mapping[e][0], 'unit': elem_mapping[e][1], 'itemcode': i, 'item': item_mapping[i], 'value': 0})
            else:
                line = data.iloc[0]
            new_df.append(line)
    return pd.DataFrame(new_df).reset_index()


def merge_with_geopandas(df):
    shapefile = 'data/gpd_maps/ne_110m_admin_0_countries.shp'
    world_map = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    world_map.columns = ['area', 'iso3code', 'geometry']
    plot_map = world_map.merge(df.drop('area', axis=1), on = 'iso3code', how ='inner')
    return plot_map