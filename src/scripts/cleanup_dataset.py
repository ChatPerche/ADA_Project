import os
from fao_ada.pre_processing.load import load_and_clean_df
from tqdm import tqdm
import click

DATA_DIR = "data/"
ITEM_GROUP_DIR = DATA_DIR + "item_groups/"
COUNTRY_DATA = DATA_DIR + "country_groups.csv"
CLEANED_DATA_DIR = "data_cleaned/"

CSV_FILES = [{"csv_file": "production/Production_Livestock_E_All_Data_(Normalized).csv",
              "item_groups": "Production_Livestock_All_data.csv",
              "country_groups": COUNTRY_DATA},
             {"csv_file": "production/Production_LivestockPrimary_E_All_Data_(Normalized).csv",
              "item_groups": "Production_Livestock_Primary_All_data.csv",
              "country_groups": COUNTRY_DATA},
             {"csv_file": "production/Production_Crops_E_All_Data_(Normalized).csv",
              "item_groups": "Production_Crops_All_data.csv",
              "country_groups": COUNTRY_DATA},
             {"csv_file": "environment/Environment_Emissions_by_Sector_E_All_Data_(Normalized).csv",
              "item_groups": "Environment_Emissions_by_sector.csv",
              "country_groups": None},
             {"csv_file": "environment/Environment_Temperature_change_E_All_Data_(Normalized).csv",
              "item_groups": None, "country_groups": None},
             {"csv_file": "emissions_land/Emissions_Land_Use_Land_Use_Total_E_All_Data_(Normalized).csv",
              "item_groups": "Emissions_Land_Use.csv", "country_groups": COUNTRY_DATA},
             {"csv_file": "emissions_agriculture/Emissions_Agriculture_Enteric_Fermentation_E_All_Data_(Normalized).csv",
              "item_groups": "Emissions_Agriculture_Enteric_Fermentation.csv", "country_groups": COUNTRY_DATA},
             {"csv_file": "emissions_agriculture/Emissions_Agriculture_Burning_Savanna_E_All_Data_(Normalized).csv",
              "item_groups": "Emissions_Agriculture_Burning_Savanna.csv", "country_groups": COUNTRY_DATA},
             {"csv_file": "emissions_agriculture/Emissions_Agriculture_Cultivated_Organic_Soils_E_All_Data_(Normalized).csv",
              "item_groups": "Emissions_Agriculture_Cultivation_organic_soils.csv", "country_groups": COUNTRY_DATA},
             {"csv_file": "emissions_agriculture/Emissions_Agriculture_Manure_Management_E_All_Data_(Normalized).csv",
              "item_groups": "Emissions_Agriculture_Manure_management.csv", "country_groups": COUNTRY_DATA},
             {"csv_file": "emissions_agriculture/Emissions_Agriculture_Manure_left_on_pasture_E_All_Data_(Normalized).csv",
              "item_groups": "Emissions_Agriculture_Manure_left_on_pasture.csv", "country_groups": COUNTRY_DATA},
             {"csv_file": "emissions_agriculture/Emissions_Agriculture_Burning_crop_residues_E_All_Data_(Normalized).csv",
              "item_groups": "Emissions_Agriculture_Burning_Crop_residues.csv", "country_groups": COUNTRY_DATA},
             {"csv_file": "emissions_agriculture/Emissions_Agriculture_Agriculture_total_E_All_Data_(Normalized).csv",
              "item_groups": "Emissions_Agriculture_All_data.csv", "country_groups": COUNTRY_DATA},
             {"csv_file": "emissions_agriculture/Emissions_Agriculture_Manure_applied_to_soils_E_All_Data_(Normalized).csv",
              "item_groups": "Emissions_Agriculture_Manure_applied_to_soils.csv", "country_groups": COUNTRY_DATA},
             {"csv_file": "emissions_agriculture/Emissions_Agriculture_Synthetic_Fertilizers_E_All_Data_(Normalized).csv",
              "item_groups": None, "country_groups": COUNTRY_DATA},
             {"csv_file": "emissions_agriculture/Emissions_Agriculture_Crop_Residues_E_All_Data_(Normalized).csv",
              "item_groups": "Emissions_Agriculture_Crop_residues.csv", "country_groups": COUNTRY_DATA},
             {"csv_file": "emissions_agriculture/Emissions_Agriculture_Energy_E_All_Data_(Norm).csv",
              "item_groups": "Emissions_Agriculture_Energy_Use.csv", "country_groups": COUNTRY_DATA},
             {"csv_file": "inputs/Inputs_Pesticides_Use_E_All_Data_(Normalized).csv", "item_groups": "Inputs_Pesticides.csv",
              "country_groups": COUNTRY_DATA},
             {"csv_fike": "emissions_agriculture/Emissions_Agriculture_Rice_Cultivation_E_All_Data_(Normalized).csv",
              "country_groups": COUNTRY_DATA, "item_groups": None},
             {"csv_file": "environment/Environment_AirClimateChange_E_All_Data.csv", 'item_groups': None, 'country_groups': None},
             {"csv_file": "population/Population_E_All_Data_(Normalized).csv", 'item_groups': None, 'country_groups': None}]


@click.command()
def main():
    """ Cleans up the dataset stored in data/, by removing all item groups, and country groups. Please call this script from root folder
        Saves the new cleaned dataset under data_cleaned/
    """
    
    if not os.path.isdir(CLEANED_DATA_DIR):
        os.mkdir(CLEANED_DATA_DIR)
    
    print(f"Cleaning dataset with {len(CSV_FILES)} csv files")
    for arg in tqdm(CSV_FILES, unit="file", ):
        csv_file = DATA_DIR + arg['csv_file']
        item_group_csv = None if arg['item_groups'] is None else ITEM_GROUP_DIR + arg['item_groups']
        cleaned_df = load_and_clean_df(csv_file, arg['country_groups'], item_group_csv)
        
        dest_dir = CLEANED_DATA_DIR + os.path.split(arg['csv_file'])[0]
        if not os.path.isdir(dest_dir):
            os.mkdir(dest_dir)
        cleaned_df.to_csv(CLEANED_DATA_DIR + arg['csv_file'], index=False)


if __name__ == "__main__":
    main()
