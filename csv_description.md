#### Emissions_Agriculture_Enteric_Fermentation_E_All_Data_(Normalized).csv
Items : 
 itemcode               item
     1107              Asses
     1126             Camels
      960      Cattle, dairy
      961  Cattle, non-dairy
     1016              Goats
     1096             Horses
     1110              Mules
      976              Sheep
     1755        All Animals
     1760  Camels and Llamas
     1757             Cattle
     1759    Mules and Asses
     1749    Sheep and Goats
      946          Buffaloes
     1051    Swine, breeding
     1049      Swine, market
     1048              Swine
     1177             Llamas

Elements : 
 elementcode                                    element         unit
        5111                                     Stocks         Head
       72244  Implied emission factor for CH4 (Enteric)  kg CH4/head
       72254                  Emissions (CH4) (Enteric)    gigagrams
       72314                Emissions (CO2eq) (Enteric)    gigagrams


Possible reshaping:
- Reduce the number of rows by adding a column for each element code
- We then get the stocks, emissions/head (CH4), total emissions CH4, and total Emissions CO2eq
- Need to reduce the number of items, as some include two items : for example cattle = cattle dairy + cattle non-dairy, camels and lamas = camels + lamas, all animals etc.. Decide which to drop depending on situation
 ------

#### Production_Livestock_E_All_Data_(Normalized).csv
Items : 
 itemcode                    item
     1107                   Asses
     1126                  Camels
      866                  Cattle
     1057                Chickens
     1016                   Goats
     1096                  Horses
     1110                   Mules
      976                   Sheep
     1746    Cattle and Buffaloes
     2029           Poultry Birds
     1749         Sheep and Goats
     1181                Beehives
      946               Buffaloes
     1068                   Ducks
     1072  Geese and guinea fowls
     1034                    Pigs
     1079                 Turkeys
     1140       Rabbits and hares
     1157         Camelids, other
     1150          Rodents, other
     1171        Animals live nes
     1083    Pigeons, other birds

Elements : 
 elementcode element       unit
        5111  Stocks       Head
        5112  Stocks  1000 Head
        5114  Stocks         No

Possible reshaping:
- Probably does not need reshaping, as each item is associated to one element (to be verifier)

 ------

#### Environment_LandCover_E_All_Data_(Normalized).csv
Items : 
 itemcode                                               item
     6970  Artificial surfaces (including urban and assoc...
     6971                                   Herbaceous crops
     6972                                        Woody crops
     6973                          Multiple or layered crops
     6983                                          Grassland
     6974                                 Tree-covered areas
     6975                                          Mangroves
     6976                                Shrub-covered areas
     6977  Shrubs and/or herbaceous vegetation, aquatic o...
     6978                   Sparsely natural vegetated areas
     6979                            Terrestrial barren land
     6980                        Permanent snow and glaciers
     6981                                Inland water bodies
     6982          Coastal water bodies and intertidal areas

Elements : 
 elementcode           element     unit
        5007   Area from MODIS  1000 ha
        5008  Area from CCI_LC  1000 ha

Possible reshaping:
- Both elements are sources from satellite imagery, maybe add a standard error betwen them or drop one, or take the mean

 ------

#### Environment_Energy_E_All_Data.csv
Items : 
 itemcode                                     item
     6740                     Bioenergy production
     6741  Energy used in agriculture and forestry

Elements : 
 elementcode                                            element unit
       72041  Bioenergy production as a % of total renewable...    %
       72040  Agriculture and forestry energy use as a % of ...    %



 ------

#### Emissions_Land_Use_Burning_Biomass_E_All_Data_(Normalized).csv
Items : 
 itemcode                      item
     6796     Humid tropical forest
     6797              Other forest
     6726             Organic soils
     6798  Burning - all categories

Elements : 
 elementcode                                            element                 unit
        7246                                        Burned Area                   ha
        7245                        Biomass burned (dry matter)               tonnes
      723011                  Emissions (N2O) (Burning biomass)            gigagrams
      722511                  Emissions (CH4) (Burning biomass)            gigagrams
      724311       Emissions (CO2eq) from N2O (Burning biomass)            gigagrams
      724411       Emissions (CO2eq) from CH4 (Burning biomass)            gigagrams
      723111                Emissions (CO2eq) (Burning biomass)            gigagrams
      722911  Implied emission factor for N2O (Burning biomass)  g N20/kg dry matter
      722411  Implied emission factor for CH4 (Burning biomass)  g CH4/kg dry matter
      719411                  Emissions (CO2) (Burning biomass)            gigagrams
      719511                    Implied emission factor for CO2  g CO2/kg dry matter


Possible reshaping: 
- Add one column for each element code to get all emissions of one item into one row
 ------

#### Emissions_Agriculture_Burning_Savanna_E_All_Data_(Normalized).csv
Items : 
 itemcode                       item
     6760                    Savanna
     6789              Woody savanna
     6791           Closed shrubland
     6792             Open shrubland
     6794                  Grassland
     6795   Burning - all categories
     6790  Savanna and woody savanna
     6793  Closed and open shrubland

Elements : 
 elementcode                                            element                 unit
        7246                                        Burned Area                   ha
        7245                        Biomass burned (dry matter)               tonnes
       72299  Implied emission factor for N2O (Burning - sav...  g N20/kg dry matter
       72249  Implied emission factor for CH4 (Burning - sav...  g CH4/kg dry matter
       72309                Emissions (N2O) (Burning - savanna)            gigagrams
       72259                Emissions (CH4) (Burning - savanna)            gigagrams
       72439     Emissions (CO2eq) from N2O (Burning - savanna)            gigagrams
       72449     Emissions (CO2eq) from CH4 (Burning - savanna)            gigagrams
       72319              Emissions (CO2eq) (Burning - savanna)            gigagrams


Possible reshaping: 
- Add one column for each element code to get all emissions of one item into one row

 ------

#### Emissions_Agriculture_Cultivated_Organic_Soils_E_All_Data_(Normalized).csv
Items : 
 itemcode                                  item
     6727                Cropland organic soils
     6728               Grassland organic soils
     6729  Cropland and grassland organic soils

Elements : 
 elementcode                                            element         unit
        5026                                               Area           ha
       72298  Implied emission factor for N2O (Cultivation o...  kg N2O-N/ha
       72308     Emissions (N2O) (Cultivation of organic soils)    gigagrams
       72318   Emissions (CO2eq) (Cultivation of organic soils)    gigagrams



 ------

#### Emissions_Agriculture_Manure_Management_E_All_Data_(Normalized).csv
Items : 
 itemcode                item
     1107               Asses
     1126              Camels
      960       Cattle, dairy
      961   Cattle, non-dairy
     1053  Chickens, broilers
     1052    Chickens, layers
     1016               Goats
     1096              Horses
     1110               Mules
      976               Sheep
     1755         All Animals
     1760   Camels and Llamas
     1757              Cattle
     1054            Chickens
     1759     Mules and Asses
     2029       Poultry Birds
     1749     Sheep and Goats
      946           Buffaloes
     1068               Ducks
     1051     Swine, breeding
     1049       Swine, market
     1079             Turkeys
     1048               Swine
     1177              Llamas

Elements : 
 elementcode                                            element           unit
        5111                                             Stocks           Head
       72386                         Manure treated (N content)             kg
       72246  Implied emission factor for CH4 (Manure manage...    kg CH4/head
       72296  Implied emission factor for N2O (Manure manage...  kg N2O-N/kg N
       72256                Emissions (CH4) (Manure management)      gigagrams
       72446     Emissions (CO2eq) from CH4 (Manure management)      gigagrams
       72346         Direct emissions (N2O) (Manure management)      gigagrams
       72366       Indirect emissions (N2O) (Manure management)      gigagrams
       72306                Emissions (N2O) (Manure management)      gigagrams
       72356       Direct emissions (CO2eq) (Manure management)      gigagrams
       72376     Indirect emissions (CO2eq) (Manure management)      gigagrams
       72436     Emissions (CO2eq) from N2O (Manure management)      gigagrams
       72316              Emissions (CO2eq) (Manure management)      gigagrams



 ------

#### Production_CropsProcessed_E_All_Data_(Normalized).csv
Items : 
 itemcode                   item
      767            Cotton lint
      329             Cottonseed
      165               Molasses
      331        Oil, cottonseed
      334           Oil, linseed
      261     Oil, olive, virgin
      290            Oil, sesame
      268         Oil, sunflower
      162  Sugar Raw Centrifugal
       51         Beer of barley
     1242       Margarine, short
      244         Oil, groundnut
      257              Oil, palm
      237           Oil, soybean
      564                   Wine
      271          Oil, rapeseed
      281         Oil, safflower
      252   Oil, coconut (copra)
      258       Oil, palm kernel
      256           Palm kernels
       60             Oil, maize

Elements : 
 elementcode     element    unit
        5510  Production  tonnes



 ------

#### Emissions_Agriculture_Rice_Cultivation_E_All_Data_(Normalized).csv
Items : 
 itemcode         item
       27  Rice, paddy

Elements : 
 elementcode                                            element       unit
        5312                                     Area harvested         ha
       72245  Implied emission factor for CH4 (Rice cultivat...   g CH4/m2
       72255                 Emissions (CH4) (Rice cultivation)  gigagrams
       72315               Emissions (CO2eq) (Rice cultivation)  gigagrams



 ------

#### Environment_Emissions_intensities_E_All_Data_(Normalized).csv
Items : 
 itemcode                       item
     1718     Cereals excluding rice
       27                Rice, paddy
      867               Meat, cattle
      882      Milk, whole fresh cow
     1017                 Meat, goat
     1020     Milk, whole fresh goat
      977                Meat, sheep
      982    Milk, whole fresh sheep
     1130    Milk, whole fresh camel
     1058              Meat, chicken
     1062        Eggs, hen, in shell
      951  Milk, whole fresh buffalo
     1035                  Meat, pig
      947              Meat, buffalo

Elements : 
 elementcode              element                 unit
       71761  Emissions intensity  kg CO2eq/kg product
        7231    Emissions (CO2eq)            gigagrams
        5510           Production               tonnes



 ------

#### Inputs_Pesticides_Use_E_All_Data_(Normalized).csv
Items : 
 itemcode                                               item
     1357                                 Pesticides (total)
     1309                                       Insecticides
     1310            Insecticides  Chlorinated Hydrocarbons
     1311                   Insecticides  Organo-phosphates
     1312                          Insecticides  Carbamates
     1313                         Insecticides  Pyrethroids
     1315                               Insecticides  Other
     1320                                         Herbicides
     1321              Herbicides  Phenoxy hormone products
     1322                             Herbicides  Triazines
     1323                                Herbicides  Amides
     1324                            Herbicides  Carbamates
     1325                       Herbicides  Dinitroanilines
     1328                        Herbicides  Sulfonyl ureas
     1329                            Herbicides  Bipiridils
     1327                                 Herbicides  Other
     1331                        Fungicides and Bactericides
     1332                           Fung & Bact  Inorganics
     1333                     Fung & Bact  Dithiocarbamates
     1334                       Fung & Bact  Benzimidazoles
     1335                  Fung & Bact  Triazoles, diazoles
     1337                                Fung & Bact  Other
     1353                     Insecticides  Seed Treatments
     1356                            Plant Growth Regulators
     1341                            Plant Growth Regulators
     1345                                       Rodenticides
     1346                     Rodenticides  Anti-coagulants
     1347                               Rodenticides  Other
     1359                               Other Pesticides nes
     1355                               Other Pesticides nes
     1314  Insecticides  Botanical products and biologicals
     1326                        Herbicides  Urea derivates
     1330                                Herbicides  Uracil
     1336                Fung & Bact  Diazines, morpholines
     1352                       Fungicides  Seed treatments
     1317                 Seed Treat Fung  Dithiocarbamates
     1318                   Seed Treat Fung  Benzimidazoles
     1319              Seed Treat Fung  Triazoles, diazoles
     1338  Seed Treat Fung  Botanical products and biolo...
     1339                            Seed Treat Fung  Other
     1342                     Seed Treat Insect  Carbamates
     1343                    Seed Treat Insect  Pyrethroids
     1344                          Seed Treat Insect  Other
     1354                                       Mineral Oils
     1316                                       Mineral Oils
     1340              Seed Treat Insect  Organo-phosphates
     1348                  Rodenticides  Cyanide Generators
     1358                                      Disinfectants
     1351                                      Disinfectants
     1350                           Rodenticides  Narcotics
     1349                     Rodenticides  Hypercalcaemics

Elements : 
 elementcode           element    unit
        5157  Agricultural Use  tonnes



 ------

#### Environment_LandUse_E_All_Data_(Normalized).csv
Items : 
 itemcode                                   item
     6621                            Arable land
     6650             Land under permanent crops
     6620                               Cropland
     6655  Land under perm. meadows and pastures
     6611    Agriculture area actually irrigated
     6690      Land area equipped for irrigation
     6610                      Agricultural land
     6646                            Forest land
     6714                         Primary Forest
     6716                         Planted Forest
     6717     Other naturally regenerated forest
     6671  Agriculture area under organic agric.

Elements : 
 elementcode                     element unit
        7208  Share in Agricultural land    %
        7209          Share in Land area    %
        7210        Share in Forest land    %



 ------

#### Environment_Pesticides_E_All_Data_(Normalized).csv
Items : 
 itemcode                item
     1357  Pesticides (total)

Elements : 
 elementcode                   element   unit
        5159  Use per area of cropland  kg/ha



 ------

#### Emissions_Agriculture_Manure_left_on_pasture_E_All_Data_(Normalized).csv
Items : 
 itemcode                item
     1107               Asses
     1126              Camels
      960       Cattle, dairy
      961   Cattle, non-dairy
     1053  Chickens, broilers
     1052    Chickens, layers
     1016               Goats
     1096              Horses
     1110               Mules
      976               Sheep
     1755         All Animals
     1760   Camels and Llamas
     1757              Cattle
     1054            Chickens
     1759     Mules and Asses
     2029       Poultry Birds
     1749     Sheep and Goats
      946           Buffaloes
     1068               Ducks
     1051     Swine, breeding
     1049       Swine, market
     1079             Turkeys
     1048               Swine
     1177              Llamas

Elements : 
 elementcode                                            element           unit
        5111                                             Stocks           Head
      723602  Indirect emissions (N2O that leaches) (Manure ...      gigagrams
      723601  Indirect emissions (N2O that volatilises) (Man...      gigagrams
       72380                 Manure left on pasture (N content)             kg
      723802    Manure left on pasture that leaches (N content)             kg
      723801  Manure left on pasture that volatilises (N con...             kg
       72290  Implied emission factor for N2O (Manure on pas...  kg N2O-N/kg N
       72340         Direct emissions (N2O) (Manure on pasture)      gigagrams
       72350       Direct emissions (CO2eq) (Manure on pasture)      gigagrams
       72360       Indirect emissions (N2O) (Manure on pasture)      gigagrams
       72370     Indirect emissions (CO2eq) (Manure on pasture)      gigagrams
       72300                Emissions (N2O) (Manure on pasture)      gigagrams
       72310              Emissions (CO2eq) (Manure on pasture)      gigagrams



 ------

#### Inputs_FertilizersArchive_E_All_Data_(Normalized).csv
Items : 
 itemcode                                           item
     1402                                        Ammonia
     1362                          Ammonium nitrate (AN)
     1379                       Ammonium Phosphat (P2o5)
     1368                         Ammonium Phosphate (N)
     1361                              Ammonium sulphate
     1363                       Ammonium SulphateNitrate
     1378                                     Basic Slag
     1372                       Calcium ammonium nitrate
     1366                              Calcium Cyanamide
     1365                                Calcium Nitrate
     1392                       Complex Fertilizer (K2o)
     1377                         Concent Superphosphate
     1390                         Crude Salts To 20% K2o
     1382                          Ground Rock Phosphate
     1389                             Muriate 20-45% K2o
     1388                           Muriate Over 45% K2o
     1360                        Nitrogenous fertilizers
     1381                        Oth Complex Fert (P2o5)
     1370                         Other Complex Fert (N)
     1369          Other nitrogenous fertilizers, n.e.c.
     1380       Other phosphatic fertilizers, n.e.c.\r\n
     1391             Other potassic fertilizers, n.e.c.
     1375                          Phosphate fertilizers
     1386                             Potash fertilizers
     1387  Potassium sulphate (sulphate of potash) (SOP)
     1376                          Single Superphosphate
     1364                                 Sodium Nitrate
     1367                                           Urea
     1818                              Total Fertilizers
     1403                                Phosphoric Acid

Elements : 
 elementcode                 element    unit
        5510              Production  tonnes
        5610         Import Quantity  tonnes
        5910         Export Quantity  tonnes
        5157        Agricultural Use  tonnes
        5751  Prices Paid by Farmers  LCU/mt



 ------

#### Inputs_FertilizersProduct_E_All_Data_(Normalized).csv
Items : 
 itemcode                                               item
     4007                                 Ammonia, anhydrous
     4003                              Ammonium nitrate (AN)
     4002                                  Ammonium sulphate
     4004  Calcium ammonium nitrate (CAN) and other mixtu...
     4022                         Diammonium phosphate (DAP)
     4030                                 Fertilizers n.e.c.
     4023                       Monoammonium phosphate (MAP)
     4021                                    NPK fertilizers
     4008              Other nitrogenous fertilizers, n.e.c.
     4024                                 Other NP compounds
     4014               Other phosphatic fertilizers, n.e.c.
     4018                 Other potassic fertilizers, n.e.c.
     4011                                     Phosphate rock
     4027                                       PK compounds
     4016       Potassium chloride (muriate of potash) (MOP)
     4025                                  Potassium nitrate
     4017      Potassium sulphate (sulphate of potash) (SOP)
     4005                                     Sodium nitrate
     4012                          Superphosphates above 35%
     4001                                               Urea
     4006          Urea and ammonium nitrate solutions (UAN)
     4026                                 Other NK compounds
     4013                             Superphosphates, other

Elements : 
 elementcode           element      unit
        5610   Import Quantity    tonnes
        5622      Import Value  1000 US$
        5910   Export Quantity    tonnes
        5922      Export Value  1000 US$
        5510        Production    tonnes
        5157  Agricultural Use    tonnes



 ------

#### Emissions_Agriculture_Burning_crop_residues_E_All_Data_(Normalized).csv
Items : 
 itemcode         item
       56        Maize
       27  Rice, paddy
      156   Sugar cane
       15        Wheat
     1712    All Crops

Elements : 
 elementcode                                            element                 unit
        7245                        Biomass burned (dry matter)               tonnes
       72297  Implied emission factor for N2O (Burning crop ...  g N20/kg dry matter
       72247  Implied emission factor for CH4 (Burning crop ...  g CH4/kg dry matter
       72307            Emissions (N2O) (Burning crop residues)            gigagrams
       72257            Emissions (CH4) (Burning crop residues)            gigagrams
       72437  Emissions (CO2eq) from N2O (Burning crop resid...            gigagrams
       72447  Emissions (CO2eq) from CH4 (Burning crop resid...            gigagrams
       72317          Emissions (CO2eq) (Burning crop residues)            gigagrams



 ------

#### Inputs_FertilizersNutrient_E_All_Data_(Normalized).csv
Items : 
 itemcode                             item
     3102      Nutrient nitrogen N (total)
     3103  Nutrient phosphate P2O5 (total)
     3104      Nutrient potash K2O (total)

Elements : 
 elementcode           element    unit
        5510        Production  tonnes
        5610   Import Quantity  tonnes
        5910   Export Quantity  tonnes
        5157  Agricultural Use  tonnes



 ------

#### Emissions_Land_Use_Forest_Land_E_All_Data_(Normalized).csv
Items : 
 itemcode                   item
     6646            Forest land
     6750  Net Forest conversion
     6749            Forest land

Elements : 
 elementcode                                      element           unit
        5110                                         Area        1000 ha
       71952              Implied emission factor for CO2  tonnes CO2/ha
       72332   Net emissions/removals (CO2) (Forest land)      gigagrams
       72172  Net emissions/removal (CO2eq) (Forest land)      gigagrams



 ------

#### Emissions_Land_Use_Grassland_E_All_Data_(Normalized).csv
Items : 
 itemcode                     item
     6728  Grassland organic soils

Elements : 
 elementcode                                    element         unit
        5026                                       Area           ha
       72411  Implied emission factor for C (Grassland)  tonnes C/ha
       72161           Net stock change (C) (Grassland)    gigagrams
       72331   Net emissions/removals (CO2) (Grassland)    gigagrams
       72171  Net emissions/removal (CO2eq) (Grassland)    gigagrams



 ------

#### Environment_LivestockPatterns_E_All_Data_(Normalized).csv
Items : 
 itemcode                   item
     1107                  Asses
     1126                 Camels
      866                 Cattle
     1057               Chickens
     1016                  Goats
     1096                 Horses
     1110                  Mules
      976                  Sheep
     1746   Cattle and Buffaloes
     1749        Sheep and Goats
     1764                Equidae
     1752  Major livestock types
      946              Buffaloes
     1034                   Pigs

Elements : 
 elementcode                                     element                   unit
        7213  Livestock units per agricultural land area                 LSU/ha
        7211                    Share in total livestock         % of total LSU
        5118                                      Stocks  Livestock units (LSU)



 ------

#### Environment_AirClimateChange_E_All_Data.csv
Items : 
 itemcode                                      item
     6730  Ammonia (NH3) emissions from agriculture

Elements : 
 elementcode                                    element unit
        7203  % of total NH3 emissions from agriculture    %



 ------

#### Emissions_Agriculture_Agriculture_total_E_All_Data_(Normalized).csv
Items : 
 itemcode                          item
     5058          Enteric Fermentation
     5059             Manure Management
     5060              Rice Cultivation
     5061         Synthetic Fertilizers
     5062       Manure applied to Soils
     5063        Manure left on Pasture
     5064                 Crop Residues
     5066       Burning - Crop residues
     5067             Burning - Savanna
     1711             Agriculture total
     1709            Agricultural Soils
     6759  Cultivation of Organic Soils

Elements : 
 elementcode                     element       unit
        7225             Emissions (CH4)  gigagrams
        7231           Emissions (CO2eq)  gigagrams
        7244  Emissions (CO2eq) from CH4  gigagrams
        7243  Emissions (CO2eq) from N2O  gigagrams
        7230             Emissions (N2O)  gigagrams



 ------

#### Production_LivestockPrimary_E_All_Data_(Normalized).csv
Items : 
 itemcode                                 item
     1062                  Eggs, hen, in shell
     1067         Eggs, hen, in shell (number)
      919                 Hides, cattle, fresh
     1182                       Honey, natural
     1137               Meat indigenous, camel
      944              Meat indigenous, cattle
     1094             Meat indigenous, chicken
     1032                Meat indigenous, goat
     1012               Meat indigenous, sheep
     1127                          Meat, camel
      867                         Meat, cattle
     1058                        Meat, chicken
     1163                           Meat, game
     1017                           Meat, goat
      977                          Meat, sheep
     1130              Milk, whole fresh camel
      882                Milk, whole fresh cow
     1020               Milk, whole fresh goat
      982              Milk, whole fresh sheep
     1185          Silk-worm cocoons, reelable
     1025                   Skins, goat, fresh
      995                  Skins, sheep, fresh
      987                         Wool, greasy
     1806                Beef and Buffalo Meat
     1783                         Eggs Primary
     1775             Meat indigenous, poultry
     1770               Meat indigenous, total
     1808                        Meat, Poultry
     1765                          Meat, Total
     1780                           Milk,Total
     1807                  Sheep and Goat Meat
     1091           Eggs, other bird, in shell
     1092  Eggs, other bird, in shell (number)
     1055                 Meat indigenous, pig
     1097                          Meat, horse
     1166                            Meat, nes
     1035                            Meat, pig
     1080                         Meat, turkey
      951            Milk, whole fresh buffalo
      999              Skins, sheep, with wool
     1120               Meat indigenous, horse
     1144              Meat indigenous, rabbit
     1087              Meat indigenous, turkey
     1141                         Meat, rabbit
     1183                              Beeswax
     1070                Meat indigenous, duck
     1077               Meat indigenous, geese
     1069                           Meat, duck
     1073          Meat, goose and guinea fowl
      957                Hides, buffalo, fresh
      972             Meat indigenous, buffalo
      947                        Meat, buffalo
     1161      Meat indigenous, other camelids
     1154             Meat indigenous, rodents
     1158                 Meat, other camelids
     1151                  Meat, other rodents
     1122                 Meat indigenous, ass
     1108                            Meat, ass
     1089                       Meat, bird nes
     1084            Meat indigenous, bird nes
     1124                Meat indigenous, mule
     1111                           Meat, mule
     1167                          Offals, nes
     1176                      Snails, not sea
     1100                          Hair, horse

Elements : 
 elementcode                        element       unit
        5313                         Laying  1000 Head
        5410                          Yield   100mg/An
        5510                     Production     tonnes
        5513                     Production    1000 No
        5320  Producing Animals/Slaughtered       Head
        5420                          Yield      hg/An
        5322                     Production       Head
        5417           Yield/Carcass Weight      hg/An
        5323                     Production  1000 Head
        5424           Yield/Carcass Weight    0.1g/An
        5321  Producing Animals/Slaughtered  1000 Head
        5318                   Milk Animals       Head
        5319                   Prod Popultn       Head
        5422                          Yield         hg
        5314                   Prod Popultn         No



 ------

#### Emissions_Land_Use_Land_Use_Total_E_All_Data_(Normalized).csv
Items : 
 itemcode             item
     5065      Forest land
     5069  Burning Biomass
     1707   Land Use total
     5070         Cropland
     6794        Grassland

Elements : 
 elementcode                         element       unit
        7233    Net emissions/removals (CO2)  gigagrams
        7217  Net emissions/removals (CO2eq)  gigagrams
        7243      Emissions (CO2eq) from N2O  gigagrams
        7244      Emissions (CO2eq) from CH4  gigagrams



 ------

#### Emissions_Agriculture_Manure_applied_to_soils_E_All_Data_(Normalized).csv
Items : 
 itemcode                item
     1107               Asses
     1126              Camels
      960       Cattle, dairy
      961   Cattle, non-dairy
     1053  Chickens, broilers
     1052    Chickens, layers
     1016               Goats
     1096              Horses
     1110               Mules
      976               Sheep
     1755         All Animals
     1760   Camels and Llamas
     1757              Cattle
     1054            Chickens
     1759     Mules and Asses
     2029       Poultry Birds
     1749     Sheep and Goats
      946           Buffaloes
     1068               Ducks
     1051     Swine, breeding
     1049       Swine, market
     1079             Turkeys
     1048               Swine
     1177              Llamas

Elements : 
 elementcode                                            element           unit
        5111                                             Stocks           Head
       72381                Manure applied to soils (N content)             kg
      723812   Manure applied to soils that leaches (N content)             kg
      723811  Manure applied to soils that volatilises (N co...             kg
       72291   Implied emission factor for N2O (Manure applied)  kg N2O-N/kg N
       72341            Direct emissions (N2O) (Manure applied)      gigagrams
       72351          Direct emissions (CO2eq) (Manure applied)      gigagrams
       72361          Indirect emissions (N2O) (Manure applied)      gigagrams
       72371        Indirect emissions (CO2eq) (Manure applied)      gigagrams
       72301                   Emissions (N2O) (Manure applied)      gigagrams
       72311                 Emissions (CO2eq) (Manure applied)      gigagrams



 ------

#### Production_Crops_E_All_Data_(Normalized).csv
Items : 
 itemcode                                          item
      221                           Almonds, with shell
      711              Anise, badian, fennel, coriander
      515                                        Apples
      526                                      Apricots
       44                                        Barley
      558                                   Berries nes
      767                                   Cotton lint
      329                                    Cottonseed
      569                                          Figs
      512                             Fruit, citrus nes
      619                              Fruit, fresh nes
      541                              Fruit, stone nes
      560                                        Grapes
      333                                       Linseed
       56                                         Maize
      568               Melons, other (inc.cantaloupes)
       79                                        Millet
      234                                     Nuts, nes
      260                                        Olives
      403                                   Onions, dry
      490                                       Oranges
      534                        Peaches and nectarines
      521                                         Pears
      223                                    Pistachios
      536                               Plums and sloes
      116                                      Potatoes
      211                                   Pulses, nes
       27                                   Rice, paddy
      328                                   Seed cotton
      289                                   Sesame seed
      723                                   Spices, nes
      157                                    Sugar beet
      156                                    Sugar cane
      267                                Sunflower seed
      463                         Vegetables, fresh nes
      222                           Walnuts, with shell
      567                                   Watermelons
       15                                         Wheat
     1817                     Cereals (Rice Milled Eqv)
     1717                                 Cereals,Total
     1804                            Citrus Fruit,Total
     1814                           Coarse Grain, Total
     1753                           Fibre Crops Primary
     1738                                 Fruit Primary
     1841                     Oilcrops, Cake Equivalent
     1732                      Oilcrops, Oil Equivalent
     1726                                  Pulses,Total
     1720                        Roots and Tubers,Total
     1729                                Treenuts,Total
     1735                            Vegetables Primary
      176                                    Beans, dry
      414                                  Beans, green
      181                 Broad beans, horse beans, dry
      358                  Cabbages and other brassicas
      426                           Carrots and turnips
      393                     Cauliflowers and broccoli
      531                                      Cherries
      530                                Cherries, sour
      220                                      Chestnut
      401                   Chillies and peppers, green
      397                        Cucumbers and gherkins
      577                                         Dates
      399                        Eggplants (aubergines)
      406                                        Garlic
      677                                          Hops
      407            Leeks, other alliaceous vegetables
      497                              Lemons and limes
      372                           Lettuce and chicory
      449                        Mushrooms and truffles
       75                                          Oats
      430                                          Okra
      402                       Onions, shallots, green
      417                                   Peas, green
      394                   Pumpkins, squash and gourds
      523                                       Quinces
       71                                           Rye
       83                                       Sorghum
      236                                      Soybeans
      373                                       Spinach
      495  Tangerines, mandarins, clementines, satsumas
      826                       Tobacco, unmanufactured
      388                                      Tomatoes
      420                    Vegetables, leguminous nes
      205                                       Vetches
      366                                    Artichokes
      486                                       Bananas
      461                                        Carobs
      191                                    Chick peas
      689                     Chillies and peppers, dry
      603                     Fruit, tropical fresh nes
      507                     Grapefruit (inc. pomelos)
      242                        Groundnuts, with shell
      201                                       Lentils
      187                                     Peas, dry
      270                                      Rapeseed
      544                                  Strawberries
       97                                     Triticale
      125                                       Cassava
      661                                  Cocoa, beans
      249                                      Coconuts
      446                                  Maize, green
      574                                    Pineapples
      136                                Taro (cocoyam)
      137                                          Yams
      782                             Bastfibres, other
      217                       Cashew nuts, with shell
      265                               Castor oil seed
      656                                 Coffee, green
      254                                Oil palm fruit
      257                                     Oil, palm
      256                                  Palm kernels
      789                                         Sisal
      122                                Sweet potatoes
      571                  Mangoes, mangosteens, guavas
      367                                     Asparagus
      572                                      Avocados
      101                                   Canary seed
      108                                  Cereals, nes
      821                               Fibre crops nes
      773                            Flax fibre and tow
      210                                        Lupins
      671                                          Maté
      339                                  Oilseeds nes
      600                                       Papayas
      748                                    Peppermint
      280                                Safflower seed
      423                                  String beans
      667                                           Tea
      275                                     Tung nuts
      225                         Hazelnuts, with shell
      552                                   Blueberries
      195                                 Cow peas, dry
      550                                      Currants
      592                                    Kiwi fruit
      292                                  Mustard seed
      587                                    Persimmons
      547                                   Raspberries
       89                                     Buckwheat
      549                                  Gooseberries
      103                                  Grain, mixed
      777                                Hemp tow waste
      296                                    Poppy seed
      554                                   Cranberries
      197                                   Pigeon peas
      489                          Plantains and others
      226                                    Areca nuts
      813                                          Coir
      720                                        Ginger
      780                                          Jute
      836                               Rubber, natural
      161                              Sugar crops, nes
      459                                 Chicory roots
      149                         Roots and tubers, nes
      135                              Yautia (cocoyam)
       94                                         Fonio
      263                        Karite nuts (sheanuts)
      224                                     Kola nuts
      687                           Pepper (piper spp.)
      702                    Nutmeg, mace and cardamoms
      216                       Brazil nuts, with shell
      754                              Pyrethrum, dried
       92                                        Quinoa
      591                                   Cashewapple
      839                                 Gums, natural
      788                                         Ramie
      336                                      Hempseed
      299                                     Melonseed
      203                                 Bambara beans
      693                            Cinnamon (canella)
      698                                        Cloves
      305                               Tallowtree seed
      692                                       Vanilla
      800                              Agave fibres nes
      378                                Cassava leaves
      809                          Manila fibre (abaca)
      778                                   Kapok fibre
      310                                   Kapok fruit
      311                            Kapokseed in shell
      277                                   Jojoba seed
      542                               Fruit, pome nes

Elements : 
 elementcode         element    unit
        5312  Area harvested      ha
        5419           Yield   hg/ha
        5510      Production  tonnes



 ------

#### Production_Indices_E_All_Data_(Normalized).csv
Items : 
 itemcode                          item
      767                   Cotton lint
      329                    Cottonseed
     1770        Meat indigenous, total
     1780                    Milk,Total
     1732      Oilcrops, Oil Equivalent
     1720        Roots and Tubers,Total
     1724                    Sugar, raw
     1739  Vegetables and Fruit Primary
     2051             Agriculture (PIN)
     1717                 Cereals,Total
     2041                   Crops (PIN)
     2054                    Food (PIN)
     2044               Livestock (PIN)
     2057                Non Food (PIN)
      257                     Oil, palm
      256                  Palm kernels

Elements : 
 elementcode                                            element    unit
         432    Gross Production Index Number (2004-2006 = 100)  Int. $
         434  Gross per capita Production Index Number (2004...  Int. $
         436      Net Production Index Number (2004-2006 = 100)  Int. $
         438  Net per capita Production Index Number (2004-2...  Int. $



 ------

#### Population_E_All_Data_(Normalized).csv
Items : 
 itemcode                       item
     3010  Population - Est. & Proj.

Elements : 
 elementcode                        element          unit
         511  Total Population - Both sexes  1000 persons
         512        Total Population - Male  1000 persons
         513      Total Population - Female  1000 persons
         551               Rural population  1000 persons
         561               Urban population  1000 persons



 ------

#### Environment_Water_E_All_Data.csv
Items : 
 itemcode                                   item
     6720  Water withdrawal for agricultural use

Elements : 
 elementcode                      element unit
        7222  % of total water withdrawal    %



 ------

#### Emissions_Land_Use_Cropland_E_All_Data_(Normalized).csv
Items : 
 itemcode                    item
     6727  Cropland organic soils

Elements : 
 elementcode                                   element         unit
        5026                                      Area           ha
       72410  Implied emission factor for C (Cropland)  tonnes C/ha
       72160           Net stock change (C) (Cropland)    gigagrams
       72330   Net emissions/removals (CO2) (Cropland)    gigagrams
       72170  Net emissions/removal (CO2eq) (Cropland)    gigagrams



 ------

#### Environment_Emissions_by_Sector_E_All_Data_(Normalized).csv
Items : 
 itemcode                                               item
     6814  Energy (energy, manufacturing and construction...
     6815                                          Transport
     6816     Residential, commercial, institutional and AFF
     6817               Industrial processes and product use
     6818                                              Waste
     6819                                      Other sources
     1711                                  Agriculture total
     6822                                   Land use sources
     6661                                             Forest
     6821                                       Energy total
     1707                                     Land Use total
     6823                                      Sources total
     6825                          Sources total excl. AFOLU
     6820                              International bunkers

Elements : 
 elementcode                                     element       unit
        7231                           Emissions (CO2eq)  Gigagrams
        7194                  Emissions (CO2eq) from CO2  Gigagrams
        7244                  Emissions (CO2eq) from CH4  Gigagrams
        7243                  Emissions (CO2eq) from N2O  Gigagrams
        7178              Emissions (CO2eq) from F-gases  Gigagrams
        7263          Share of sector in total emissions          %
        7264      Share of sector in total CO2 emissions          %
        7265      Share of sector in total CH4 emissions          %
        7266      Share of sector in total N2O emissions          %
        7267            Share of CO2 in sector emissions          %
        7268            Share of CH4 in sector emissions          %
        7269            Share of N2O in sector emissions          %
        7180        Share of F-gases in sector emissions  Gigagrams
        7179  Share of sector in total F-gases emissions  Gigagrams



 ------

#### Inputs_LandUse_E_All_Data_(Normalized).csv
Items : 
 itemcode                                               item
     6600                                       Country area
     6601                                          Land area
     6602                                        Agriculture
     6610                                  Agricultural land
     6620                                           Cropland
     6621                                        Arable land
     6630                         Land under temporary crops
     6640                         Land with temporary fallow
     6650                         Land under permanent crops
     6655              Land under perm. meadows and pastures
     6659            Perm. meadows & pastures - Nat. growing
     6663                                           Forestry
     6646                                        Forest land
     6714                                     Primary Forest
     6717                 Other naturally regenerated forest
     6716                                     Planted Forest
     6670                                         Other land
     6690                  Land area equipped for irrigation
     6611                Agriculture area actually irrigated
     6671              Agriculture area under organic agric.
     6672                 Agriculture area certified organic
     6633              Land under temp. meadows and pastures
     6680                                      Inland waters
     6773                                     Coastal waters
     6694                   Cropland area actually irrigated
     6668                 Cropland area under organic agric.
     6669                    Cropland area certified organic
     6656              Perm. meadows & pastures - Cultivated
     6762                          Land used for aquaculture
     6657      Perm. meadows & pastures area actually irrig.
     6649                        Land under protective cover
     6681  Perm. meadows & pastures area under organic ag...
     6616                       Land area actually irrigated
     6664           Cropland area under conventional tillage
     6665           Cropland area under conservation tillage
     6666             Cropland area under zero or no tillage
     6775                         Farm buildings & farmyards
     6682    Perm. meadows & pastures area certified organic
     6767  Inland waters used for aquac. or holding facil...
     6643                      Exclusive Economic Zone (EEZ)
     6641  Coastal waters used for aquac. or holding faci...
     6642          Coastal waters used for capture fisheries
     6644          EEZ used for aquac. or holding facilities
     6771           Inland waters used for capture fisheries
     6645                     EEZ used for capture fisheries

Elements : 
 elementcode                         element            unit
        5110                            Area         1000 ha
       72151  Carbon stock in living biomass  million tonnes



 ------

#### Environment_Soil_E_All_Data.csv
Items : 
 itemcode  item
     6709  Soil

Elements : 
 elementcode                                            element     unit
        7219  Average soil erosion expressed in GLASOD erosi...  degrees
        7220  Average land degradation in GLASOD erosion degree  degrees
        7221  Average carbon content in the topsoil as a % i...        %



 ------

#### Environment_LivestockManure_E_All_Data_(Normalized).csv
Items : 
 itemcode                item
     1107               Asses
     1126              Camels
      960       Cattle, dairy
      961   Cattle, non-dairy
     1053  Chickens, broilers
     1052    Chickens, layers
     1016               Goats
     1096              Horses
     1110               Mules
      976               Sheep
     1755         All Animals
     1760   Camels and Llamas
     1757              Cattle
     1054            Chickens
     1759     Mules and Asses
     2029       Poultry Birds
     1749     Sheep and Goats
      946           Buffaloes
     1068               Ducks
     1051     Swine, breeding
     1049       Swine, market
     1079             Turkeys
     1048               Swine
     1177              Llamas

Elements : 
 elementcode                                            element  unit
        5111                                             Stocks  Head
       72538              Amount excreted in manure (N content)    kg
       72380                 Manure left on pasture (N content)    kg
      723801  Manure left on pasture that volatilises (N con...    kg
      723802    Manure left on pasture that leaches (N content)    kg
       72386                         Manure treated (N content)    kg
       72539             Losses from manure treated (N content)    kg
       72381                Manure applied to soils (N content)    kg
      723811  Manure applied to soils that volatilises (N co...    kg
      723812   Manure applied to soils that leaches (N content)    kg



 ------

#### Emissions_Agriculture_Synthetic_Fertilizers_E_All_Data_(Normalized).csv
Items : 
 itemcode                            item
     1360         Nitrogenous fertilizers
     3102     Nutrient nitrogen N (total)
     3107  Synthetic Nitrogen fertilizers

Elements : 
 elementcode                                            element             unit
        5163                                   Agricultural Use               kg
      516202   Nitrogen fertilizer content applied that leaches  kg of nutrients
      516201  Nitrogen fertilizer content applied that volat...  kg of nutrients
        5162                      Agricultural Use in nutrients  kg of nutrients
       72293  Implied emission factor for N2O (Synthetic fer...    kg N2O-N/kg N
       72343     Direct emissions (N2O) (Synthetic fertilizers)        gigagrams
       72353   Direct emissions (CO2eq) (Synthetic fertilizers)        gigagrams
      723632  Indirect emissions (N2O that leaches) (Synthet...        gigagrams
      723631  Indirect emissions (N2O that volatilises) (Syn...        gigagrams
       72363   Indirect emissions (N2O) (Synthetic fertilizers)        gigagrams
       72373  Indirect emissions (CO2eq) (Synthetic fertiliz...        gigagrams
       72303            Emissions (N2O) (Synthetic fertilizers)        gigagrams
       72313          Emissions (CO2eq) (Synthetic fertilizers)        gigagrams



 ------

#### Environment_Fertilizers_E_All_Data_(Normalized).csv
Items : 
 itemcode                             item
     3102      Nutrient nitrogen N (total)
     3103  Nutrient phosphate P2O5 (total)
     3104      Nutrient potash K2O (total)

Elements : 
 elementcode                   element   unit
        5159  Use per area of cropland  kg/ha



 ------

#### Forestry_E_All_Data_(Normalized).csv
Items : 
 itemcode                                               item
     1877                    Forest products (export/import)
     1861                                          Roundwood
     1862                 Roundwood, coniferous (production)
     1863             Roundwood, non-coniferous (production)
     1864                                          Wood fuel
     1627                              Wood fuel, coniferous
     1628                          Wood fuel, non-coniferous
     1629             Wood fuel, all species (export/import)
     1865                               Industrial roundwood
     1866                   Industrial roundwood, coniferous
     1651   Industrial roundwood, coniferous (export/import)
     1867               Industrial roundwood, non-coniferous
     1657  Industrial roundwood, non-coniferous tropical ...
     1670  Industrial roundwood, non-coniferous non-tropi...
     1868                            Sawlogs and veneer logs
     1601                Sawlogs and veneer logs, coniferous
     1604            Sawlogs and veneer logs, non-coniferous
     1871                         Other industrial roundwood
     1623  Other industrial roundwood, coniferous (produc...
     1626  Other industrial roundwood, non-coniferous (pr...
     1630                                      Wood charcoal
     1695                 Wood chips, particles and residues
     1619                           Wood chips and particles
     1620                                      Wood residues
     1872                                           Sawnwood
     1632                               Sawnwood, coniferous
     1633                       Sawnwood, non-coniferous all
     1634                                      Veneer sheets
     1873                                  Wood-based panels
     1640                                            Plywood
     1646                 Particle board and OSB (1961-1994)
     1697                                     Particle board
     1606                                                OSB
     1874                                         Fibreboard
     1647                                          Hardboard
     1648                                            MDF/HDF
     1650                                   Other fibreboard
     1649                 Fibreboard, compressed (1961-1994)
     1879                                Total fibre furnish
     1878                                     Pulp for paper
     1875                                          Wood pulp
     1654                               Mechanical wood pulp
     1859          Wood pulp, excluding mechanical wood pulp
     1655                            Semi-chemical wood pulp
     1656                                 Chemical wood pulp
     1663             Chemical wood pulp, sulphate, bleached
     1661             Chemical wood pulp, sulphite, bleached
     1667                               Dissolving wood pulp
     1668                   Pulp from fibres other than wood
     1609                               Recovered fibre pulp
     1669                                    Recovered paper
     1876                               Paper and paperboard
     2042                                     Graphic papers
     1671                                          Newsprint
     1860          Paper and paperboard, excluding newsprint
     1674                        Printing and writing papers
     1612  Printing and writing papers, uncoated, mechanical
     1615   Printing and writing papers, uncoated, wood free
     1616                Printing and writing papers, coated
     1675                         Other paper and paperboard
     1676                      Household and sanitary papers
     2043                     Packaging paper and paperboard
     1681        Wrapping and packaging paper and paperboard
     1617                                     Case materials
     1618                                        Cartonboard
     1621                                    Wrapping papers
     1622                  Other papers mainly for packaging
     1683  Other paper and paperboard n.e.s. (not elsewhe...
     2038  Pulpwood, round and split, all species (produc...
     1602  Pulpwood, round and split, coniferous (product...
     1603  Pulpwood, round and split, non-coniferous (pro...
     1696                Wood pellets and other agglomerates
     1693                                       Wood pellets
     1662           Chemical wood pulp, sulphate, unbleached
     1660           Chemical wood pulp, sulphite, unbleached
     1870                 Pulpwood and particles (1961-1997)
     1608  Pulpwood and particles, coniferous (production...
     1611  Pulpwood and particles, non-coniferous (produc...
     1625  Other industrial roundwood, all species (expor...
     1694                                 Other agglomerates
     1614  Pulpwood, round and split, all species (export...

Elements : 
 elementcode          element      unit
        5622     Import Value  1000 US$
        5922     Export Value  1000 US$
        5516       Production        m3
        5616  Import Quantity        m3
        5916  Export Quantity        m3
        5510       Production    tonnes
        5610  Import Quantity    tonnes
        5910  Export Quantity    tonnes



 ------

#### Emissions_Agriculture_Crop_Residues_E_All_Data_(Normalized).csv
Items : 
 itemcode         item
       44       Barley
       56        Maize
       79       Millet
      116     Potatoes
       27  Rice, paddy
       15        Wheat
     1712    All Crops
      176   Beans, dry
       75         Oats
       71          Rye
       83      Sorghum
      236     Soybeans

Elements : 
 elementcode                                          element             unit
       72392                         Residues (Crop residues)  kg of nutrients
       72292  Implied emission factor for N2O (Crop residues)    kg N2O-N/kg N
       72342           Direct emissions (N2O) (Crop residues)        gigagrams
       72352         Direct emissions (CO2eq) (Crop residues)        gigagrams
       72362         Indirect emissions (N2O) (Crop residues)        gigagrams
       72372       Indirect emissions (CO2eq) (Crop residues)        gigagrams
       72302                  Emissions (N2O) (Crop residues)        gigagrams
       72312                Emissions (CO2eq) (Crop residues)        gigagrams



 ------

#### Production_LivestockProcessed_E_All_Data_(Normalized).csv
Items : 
 itemcode                         item
      983  Butter and ghee, sheep milk
      886             Butter, cow milk
     1021           Cheese of goat mlk
      984           Cheese, sheep milk
      888            Milk, skimmed cow
     1186                     Silk raw
     1811              Butter and Ghee
     1745           Cheese (All Kinds)
      901       Cheese, whole cow milk
      904     Cheese, skimmed cow milk
     1043                         Lard
      885                  Cream fresh
      887  Ghee, butteroil of cow milk
      898          Milk, skimmed dried
      889        Milk, whole condensed
      897            Milk, whole dried
      894       Milk, whole evaporated
     1225                       Tallow
      900                    Whey, dry
     1816      Evaporat&Condensed Milk
     1809     Skim Milk&Buttermilk,Dry
      899         Milk, dry buttermilk
      896      Milk, skimmed condensed
      895     Milk, skimmed evaporated
      953        Ghee, of buffalo milk
      890              Whey, condensed
      891                      Yoghurt
      952         Butter, buffalo milk
      955         Cheese, buffalo milk
     1022           Butter of goat mlk

Elements : 
 elementcode     element    unit
        5510  Production  tonnes



 ------

#### Environment_Temperature_change_E_All_Data_(Normalized).csv
Items : 
Empty DataFrame
Columns: []
Index: []

Elements : 
 elementcode             element unit
        7271  Temperature change   °C
        6078  Standard Deviation   °C



 ------

#### Emissions_Agriculture_Energy_E_All_Data_(Norm).csv
Items : 
 itemcode                                               item
     6801                                     Gas-Diesel oil
     6800                                     Motor Gasoline
     6802                        Natural gas (including LNG)
     6805                      Liquefied petroleum gas (LPG)
     6804                                           Fuel oil
     6809                                               Coal
     6807                                        Electricity
     6803                  Gas-diesel oils used in fisheries
     6806                         Fuel oil used in fisheries
     6808                        Energy for power irrigation
     6810  Transport fuel used in agriculture (excl. fish...
     6813                                       Total Energy
     6811                             Energy used in fishery

Elements : 
 elementcode                              element         unit
       72184           Consumption in Agriculture    Terajoule
      719610      Implied emission factor for CH4        Kg/TJ
      722510             Emissions (CH4) (Energy)    Gigagrams
      724410  Emissions (CO2eq) from CH4 (Energy)    Gigagrams
      719710      Implied emission factor for N2O        Kg/TJ
      723010             Emissions (N2O) (Energy)    Gigagrams
      724310  Emissions (CO2eq) from N2O (Energy)    Gigagrams
      719510      Implied emission factor for CO2        Kg/TJ
      719410             Emissions (CO2) (Energy)    Gigagrams
      723110           Emissions (CO2eq) (Energy)    Gigagrams
       72182           Consumption in Agriculture  million kWh
      719509      Implied emission factor for CO2        g/kWh



 ------

