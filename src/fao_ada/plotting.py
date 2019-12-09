import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from fao_ada.utils import merge_with_geopandas
from fao_ada.pre_processing.grouping import groupby_all_items_sum

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
