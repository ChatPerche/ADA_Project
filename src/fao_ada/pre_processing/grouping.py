import pandas as pd
from typing import Optional, List
import numpy as np
from fao_ada.utils import get_items_only_in_itemgroup
MISSING_FLAG = "M"
COMPLETE_FLAG = "C"


def get_flag(values, itemcodes):
    if len(values) != len(itemcodes) or pd.isna(values).any():
        return MISSING_FLAG
    return COMPLETE_FLAG


def groupby_item_groups(df: pd.DataFrame, itemgroups: pd.DataFrame,
                        drop_elements: Optional[List[str]] = None, except_: Optional[dict] = None) -> pd.DataFrame:
    """ This functions groups all the items by itemgroup (Be careful that units match , because aggregation is done by sum)

    :param df:
    :param grpd:
    :param drop_elements
    :return:
    """
    new_df = []
    grpd = itemgroups.groupby(['itemgroupcode', 'itemgroup'])['itemcode'].apply(set)
    
    for group, codes in grpd.iteritems():
        itemgroupcode, itemgroup = group
        if except_ is not None and itemgroupcode in except_:
            codes = get_items_only_in_itemgroup(itemgroups, itemgroupcode)
            itemgroup = except_[itemgroupcode][0]
            itemgroupcode = except_[itemgroupcode][1]
            
        fltrd = df[df['itemcode'].isin(codes)].drop(columns=['item', 'itemcode'])
        fltrd = fltrd.groupby(['areacode', 'area', 'elementcode', 'element', 'unit', 'year'])['value'].apply(
                list).reset_index()
        fltrd = fltrd.assign(itemcode=itemgroupcode).assign(item=itemgroup)
        
        fltrd = fltrd.assign(flag=fltrd['value'].apply(lambda x: get_flag(x, codes)))
        fltrd['value'] = fltrd['value'].apply(np.nansum)
        new_df.append(fltrd)
    new_df = pd.concat(new_df, sort=False).reset_index(drop=True)
    
    if drop_elements is not None:
        new_df = new_df[~new_df.elementcode.isin(drop_elements)]
    if except_ is not None:
        new_df = new_df[~new_df.itemcode.isin(except_)]
    return new_df


def groupby_country_groups(df: pd.DataFrame, country_groups: pd.DataFrame,
                           drop_elements: Optional[List[str]] = None,
                           keep_elements: Optional[List[str]] = None) -> pd.DataFrame:
    new_df = []
    country_groups = country_groups.groupby(['countrygroupcode', 'countrygroup'])['areacode'].apply(set)
    
    for group, codes in country_groups.iteritems():
        countrygroupcode, countrygroup = group
        
        fltrd = df[df['areacode'].isin(codes)].drop(columns=['area', 'areacode'])
        
        fltrd = fltrd.groupby(['itemcode', 'item', 'elementcode', 'element', 'unit', 'year'])['value'].apply(
                list).reset_index()
        fltrd = fltrd.assign(areacode=countrygroupcode).assign(area=countrygroup)
        
        fltrd = fltrd.assign(flag=fltrd['value'].apply(lambda x: get_flag(x, codes)))
        fltrd['value'] = fltrd['value'].apply(np.nansum)
        new_df.append(fltrd)
    
    df = pd.concat(new_df, sort=False).reset_index(drop=True)
    if drop_elements is not None:
        df = df[~df.elementcode.isin(drop_elements)]
    
    if keep_elements is not None:
        df = df[df.elementcode.isin(keep_elements)]
    df['year'] = df.year.astype('int')
    return df


def groupby_all_items_sum(df: pd.DataFrame) -> pd.DataFrame:
    df = df.groupby(['areacode', 'area', 'elementcode', 'element', 'unit', 'year'])[
        'value'].sum().reset_index()  # Group all items
    return df
