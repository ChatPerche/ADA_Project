import pandas as pd

MISSING_FLAG = "M"
COMPLETE_FLAG = "C"


def get_flag(values, itemcodes):
    if len(values) != len(itemcodes) or pd.isna(values).any():
        return MISSING_FLAG
    return COMPLETE_FLAG


def groupby_item_groups(df: pd.DataFrame, item_groups: pd.DataFrame) -> pd.DataFrame:
    """ This functions groups all the items by itemgroup (Be careful that units match , because aggregation is done by sum)

    :param df:
    :param item_groups:
    :return:
    """
    new_df = []
    item_groups = item_groups.groupby(['itemgroupcode', 'itemgroup'])['itemcode'].apply(set)
    
    for group, codes in item_groups.iteritems():
        itemgroupcode, itemgroup = group
        fltrd = df[df['itemcode'].isin(codes)].drop(columns=['item', 'itemcode'])
        fltrd = fltrd.groupby(['areacode', 'area', 'elementcode', 'element', 'unit', 'year'])['value'].apply(
                list).reset_index()
        fltrd = fltrd.assign(itemcode=itemgroupcode).assign(item=itemgroup)
        
        fltrd = fltrd.assign(flag=fltrd['value'].apply(lambda x: get_flag(x, codes)))
        fltrd['value'] = fltrd['value'].apply(sum)
        new_df.append(fltrd)
    
    return pd.concat(new_df, sort=False).reset_index()


def groupby_country_groups(df: pd.DataFrame, country_groups: pd.DataFrame) -> pd.DataFrame:
    new_df = []
    country_groups = country_groups.groupby(['countrygroupcode', 'countrygroup'])['areacode'].apply(set)
    
    for group, codes in country_groups.iteritems():
        countrygroupcode, countrygroup = group
        
        fltrd = df[df['areacode'].isin(codes)].drop(columns=['area', 'areacode'])
        
        fltrd = fltrd.groupby(['itemcode', 'item', 'elementcode', 'element', 'unit', 'year'])['value'].apply(
                list).reset_index()
        fltrd = fltrd.assign(areacode=countrygroupcode).assign(area=countrygroup)
        
        fltrd = fltrd.assign(flag=fltrd['value'].apply(lambda x: get_flag(x, codes)))
        fltrd['value'] = fltrd['value'].apply(sum)
        new_df.append(fltrd)
    
    return pd.concat(new_df, sort=False).reset_index()
