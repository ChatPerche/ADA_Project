import pandas as pd
import gc

data_folder = 'data/'

filenames = [
"Emissions_Agriculture_Agriculture_total_E_All_Data_(Normalized).csv",
"Emissions_Agriculture_Burning_Savanna_E_All_Data_(Normalized).csv",
"Emissions_Agriculture_Burning_crop_residues_E_All_Data_(Normalized).csv",
"Emissions_Agriculture_Crop_Residues_E_All_Data_(Normalized).csv",
"Emissions_Agriculture_Cultivated_Organic_Soils_E_All_Data_(Normalized).csv",
"Emissions_Agriculture_Energy_E_All_Data_(Norm).csv",
"Emissions_Agriculture_Enteric_Fermentation_E_All_Data_(Normalized).csv",
"Emissions_Agriculture_Manure_Management_E_All_Data_(Normalized).csv",
"Emissions_Agriculture_Manure_applied_to_soils_E_All_Data_(Normalized).csv",
"Emissions_Agriculture_Manure_left_on_pasture_E_All_Data_(Normalized).csv",
"Emissions_Agriculture_Rice_Cultivation_E_All_Data_(Normalized).csv",
"Emissions_Agriculture_Synthetic_Fertilizers_E_All_Data_(Normalized).csv",
"Emissions_Land_Use_Burning_Biomass_E_All_Data_(Normalized).csv",
"Emissions_Land_Use_Cropland_E_All_Data_(Normalized).csv",
"Emissions_Land_Use_Forest_Land_E_All_Data_(Normalized).csv",
"Emissions_Land_Use_Grassland_E_All_Data_(Normalized).csv",
"Emissions_Land_Use_Land_Use_Total_E_All_Data_(Normalized).csv",
"Environment_AirClimateChange_E_All_Data.csv",
"Environment_Emissions_by_Sector_E_All_Data_(Normalized).csv",
"Environment_Emissions_intensities_E_All_Data_(Normalized).csv",
"Environment_Energy_E_All_Data.csv",
"Environment_Fertilizers_E_All_Data_(Normalized).csv",
"Environment_LandCover_E_All_Data_(Normalized).csv",
"Environment_LandUse_E_All_Data_(Normalized).csv",
"Environment_LivestockManure_E_All_Data_(Normalized).csv",
"Environment_LivestockPatterns_E_All_Data_(Normalized).csv",
"Environment_Pesticides_E_All_Data_(Normalized).csv",
"Environment_Soil_E_All_Data.csv",
"Environment_Temperature_change_E_All_Data_(Normalized).csv",
"Environment_Water_E_All_Data.csv",
"Forestry_E_All_Data_(Normalized).csv",
"Inputs_FertilizersArchive_E_All_Data_(Normalized).csv",
"Inputs_FertilizersNutrient_E_All_Data_(Normalized).csv",
"Inputs_FertilizersProduct_E_All_Data_(Normalized).csv",
"Inputs_LandUse_E_All_Data_(Normalized).csv",
"Inputs_Pesticides_Use_E_All_Data_(Normalized).csv",
"Population_E_All_Data_(Normalized).csv",
"Production_CropsProcessed_E_All_Data_(Normalized).csv",
"Production_Crops_E_All_Data_(Normalized).csv",
"Production_Indices_E_All_Data_(Normalized).csv",
"Production_LivestockPrimary_E_All_Data_(Normalized).csv",
"Production_LivestockProcessed_E_All_Data_(Normalized).csv",
"Production_Livestock_E_All_Data_(Normalized).csv",
]


def create_mappings(verbose = False):

    # Asserts that intersection indices have identical rows in both DataFrames
    # Returns the merged dataframe with no duplicates
    def merge_df(df_1,df_2):

        intersecting_indices = df_1.index.intersection(df_2.index)
        df_1_on_intersect    = df_1.loc[intersecting_indices,:]
        df_2_on_intersect    = df_2.loc[intersecting_indices,:]

        if len(intersecting_indices) is not 0 and \
            not df_1_on_intersect.equals(df_2_on_intersect):

            if verbose:

                union = df_1_on_intersect.append(df_2_on_intersect)
                conflicts = union.loc[union.duplicated(keep=False) == False]

                print("\n ----------  WARNING   ---------")
                print("Conflict in building mapping -- first values will be kept:")
                print(conflicts)
                print(" --------------------------------- \n")

            return df_1.append(df_2.drop(intersecting_indices).drop_duplicates())

        else:
            return df_1.append(df_2).drop_duplicates()

    area_mapping = pd.DataFrame(columns=['Area Code', 'Area']).set_index('Area Code')
    elem_mapping = pd.DataFrame(columns=['Element Code','Element']).set_index('Element Code')
    item_mapping = pd.DataFrame(columns=['Item Code','Item']).set_index('Item Code')

    # Iterate through our different CSVs.
    for file in filenames: 

        df = pd.read_csv(data_folder+file,encoding='latin-1')

        to_append_area = None
        if 'Area' in df.columns:
            to_append_area = df[['Area Code','Area']]
        elif 'Country Code' in df.columns:
            to_append_area = df[['Country Code','Country']].rename(columns={'Country Code':'Area Code','Country':'Area'})
        elif 'CountryCode' in df.columns:
            to_append_area = df[['CountryCode', 'Country']].rename(columns={'CountryCode': 'Area Code', 'Country': 'Area'})
        else: 
            assert(False)
            
        to_append_area = to_append_area.drop_duplicates().set_index('Area Code',verify_integrity=True)
        area_mapping   = merge_df(area_mapping,to_append_area)

        del [[to_append_area]]
        gc.collect()
        
        to_append_item = None
        if 'Item Code' in df.columns:
            to_append_item = df[['Item Code','Item']]
        elif 'ItemCode' in df.columns:
            to_append_item = df[['ItemCode', 'Item']].rename(columns={'ItemCode':'Item Code'})
        elif verbose:
            print("\n ----------  WARNING   ---------")
            print("No item column found in file "+file+" columns")
            print(df.columns)
            print(" --------------------------------- \n")

        if to_append_item is not None:

            to_append_item = to_append_item.drop_duplicates().set_index('Item Code')
            item_mapping   = merge_df(item_mapping,to_append_item)

            del [[to_append_item]]
            gc.collect()

        if 'Element Code' in df.columns:
            to_append_elem = df[['Element Code','Element']]
        elif 'ElementCode' in df.columns:
            to_append_elem = df[['ElementCode', 'Element']].rename(columns={'ElementCode': 'Element Code'})
        else:
            assert(False)

        to_append_elem = to_append_elem.drop_duplicates().set_index('Element Code')
        elem_mapping   = merge_df(elem_mapping,to_append_elem)

        del [[to_append_elem,df]]
        gc.collect()

    return area_mapping, elem_mapping, item_mapping

