from fao_ada.pre_processing.load import load_dataframe
from fao_ada.utils import merge_with_geopandas

# could add minimum and maximum years for custom plotting range
# needs df with columns VALUE and AREA and YEAR

def plot_world_map_slider(df, shapefile, filename, title, heatbar_text):
    
    regions = load_dataframe("data/country_groups.csv")
    regions.columns = ["countrygroupcode","countrygroup","countrycode","country","m49code","iso2code","iso3code"]
    regions = regions.rename({"country":"area"}, axis =1)\
                        .drop(["countrygroup","countrygroupcode","countrycode","m49code","iso2code"], axis = 1)

    df = df.groupby(["area","year","unit"])\
                        .agg({"value":"sum"}).reset_index()\
                        .drop_duplicates()\
                        .merge(regions, on = "area")\

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
