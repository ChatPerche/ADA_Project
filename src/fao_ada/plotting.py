import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go

from fao_ada.utils import merge_with_geopandas
from fao_ada.pre_processing.grouping import groupby_all_items_sum
from fao_ada.pre_processing.load import load_dataframe


def line_plot_single_element_single_area(df, elementcode, areacode, title, ylabel, figsize=(15, 8)):
    fig, ax = plt.subplots(figsize=figsize)
    df = df[(df.elementcode == elementcode) & (df.areacode == areacode)]
    g = sns.lineplot(x='year', y='value', data=df, hue='item', ax=ax)
    g.legend(loc='center', bbox_to_anchor=(0.5, -0.2), ncol=2)
    ax.set_title(title)
    ax.set_ylabel(ylabel)


def plot_pie(vals, labels, ax, title, with_labels=False):
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    
    def func(pct, allvals):
        absolute = int(pct / 20. * np.sum(allvals))
        if pct > 1:
            return "{:.1f}%".format(pct, absolute)
        return ""
    
    if with_labels:
        ax.pie(vals, labels=labels, autopct=lambda pct: func(pct, vals), radius=2)
    else:
        ax.pie(vals, autopct=lambda pct: func(pct, vals), radius=2)
    ax.add_artist(my_circle)
    ax.set_title(title, y=1.4)


def add_zero_values(df):
    new_df = []
    for i in df.itemcode.unique():
        item = df[df.itemcode == i]['item'].iloc[0]
        
        for e in df.elementcode.unique():
            element, unit = df[(df.elementcode == e)][['element', 'unit']].iloc[0]
            
            data = df[(df.elementcode == e) & (df.itemcode == i)]
            if len(data) == 0:
                line = pd.Series({
                    'elementcode': e, 'element': element, 'unit': unit,
                    'itemcode': i, 'item': item, 'value': 0
                    })
            else:
                line = data.iloc[0]
            new_df.append(line)
    return pd.DataFrame(new_df).reset_index()


def plot_elements_pie_single_area(df, elementcodes, areacode, suptitle, figsize=(20, 20), y_title=0.68):
    df = df[(df.elementcode.isin(elementcodes)) & (df.areacode == areacode)].drop(columns=['area', 'areacode'])
    df = add_zero_values(df)
    
    n_cols = len(elementcodes)
    fig, axs = plt.subplots(figsize=figsize, ncols=n_cols)
    for i, code in enumerate(df.elementcode.unique()):
        ax = axs[i]
        tmp = df[df.elementcode == code]
        title = f"{tmp.element.unique()[0]}"
        
        tmp = tmp.groupby(['item'])['value'].mean().reset_index()
        labels, vals = tmp.item.values, tmp.value.values
        plot_pie(vals, labels, ax, title)
    plt.subplots_adjust(wspace=1.2)
    plt.legend(labels, loc='center', bbox_to_anchor=(-1.8, -0.7), ncol=2)
    fig.suptitle(suptitle, x=0.5, y=y_title, size=15)


def plot_stacked_bar_single_area_single_element(df, elementcode, areacode, title, ylabel, figsize=(15, 7),
                                                bbox=(0.85, -0.1), width=0.2):
    df = df[(df.elementcode == elementcode) & (df.areacode == areacode)]
    
    ind = np.arange(df.year.nunique())
    fig, ax = plt.subplots(figsize=figsize)
    below = None
    bars = []
    for i in df.itemcode.unique():
        values = []
        
        for y in sorted(df.year.unique()):
            tmp = df[(df.itemcode == i) & (df.year == y)]
            if len(tmp) == 0:
                values.append(0)
            else:
                values.append(tmp.iloc[0]['value'])
        
        bottom = None
        if below is not None:
            bottom = np.sum(below, axis=0)
            below.append(values)
        else:
            below = [values]
        bar = ax.bar(ind, values, width, bottom=bottom)
        bars.append(bar)
    
    plt.xticks(ind, sorted(df.year.unique()), rotation='vertical')
    
    plt.legend(tuple(bars), df.item.unique(),
               bbox_to_anchor=bbox, loc='upper right', ncol=2)
    ax.set_title(title)
    ax.set_ylabel(ylabel)


def plot_maps(df, elementcodes, countries_df, year, shapefile, titles, itemcodes=None, figsize=(15, 15)):
    fig, ax = plt.subplots(figsize=figsize, nrows=len(elementcodes))
    df = df[df.elementcode.isin(elementcodes)]
    if itemcodes is not None:
        df = df[df.itemcode.isin(itemcodes)]

    df = groupby_all_items_sum(df)
    
    df = df.merge(countries_df[['areacode', 'iso3code']], left_on='areacode', right_on='areacode')
    
    for i, e in enumerate(elementcodes):
        tmp = df[(df.elementcode == e) & (df.year == year)]
        unit = tmp.unit.iloc[0]
        tmp = merge_with_geopandas(tmp, shapefile)
        tmp.plot(column='value', cmap='OrRd', ax=ax[i], legend=True,
                 legend_kwds={'label': unit, 'orientation': "vertical"})
        ax[i].set_title(titles[e])

        


def plot_world_map_slider(df, filename, title, heatbar_text):
    
    shapefile = "data/gpd_maps/ne_110m_admin_0_countries.shp"
       
    regions = load_dataframe("data/country_groups.csv")
    regions.columns = ["countrygroupcode","countrygroup","countrycode","country","m49code","iso2code","iso3code"]
    regions = regions.rename({"country":"area"}, axis =1)\
                        .drop(["countrygroup","countrygroupcode","countrycode","m49code","iso2code"], axis = 1)

    df = df.merge(regions, on = "area")

    df = merge_with_geopandas(df, shapefile)

    
    year_max = int(df.year.max())
    year_min = int(df.year.min())
    total_years =  year_max - year_min 

    fig = go.Figure()

    for year in range(year_min, year_max):
        current_map = df[(df.year == year)]


        fig.add_trace(go.Choropleth(
            locations = current_map['iso3code'],
            z = current_map['value'],
            text = current_map['area'],
            colorscale = 'Portland',
            autocolorscale=False,
            reversescale=False,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title = heatbar_text ))
        fig.update_layout(title=dict(
                            text = title,
                            y= 0.9,
                            x= 0.5),
                        geo=dict(
                            showframe=False,
                            showcoastlines=False,
                            projection_type='equirectangular'),
                        annotations = [dict(
                            x=0.5,
                            y=-0.1,
                            text='Source: FAOSTAT',
                            showarrow = False)] )

    steps = list()
    for year in range(total_years):
        step = dict(
            method='restyle',
            args=['visible', [False] * total_years],
            label=year_min+ year
        )
        step['args'][1][year] = True
        steps.append(step)

    sliders = [dict(
        active=0,
        steps=steps)]

    fig.update_layout(
        sliders=sliders
    )

    plotly.offline.plot(fig, filename= filename + '.html', auto_open = False)
    fig.show()