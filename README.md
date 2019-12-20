# Environmental Impact of Agricultural Practices in the World. 

# Abstract
In 2017, agriculture accounted for 9% of global Greenhouse gas emissions around the world. Feeding 7 billion people is indeed one of the most important tasks of human kind, and those practices have been around for millennia, but have, without a doubt, changed quite a bit. The UN's Food and Agriculture Organization provides a rich and open dataset called FAOSTAT, containing statistics on agricultural production and emissions, fertilizer use, trade,  prices, food security and annual population by country from 1961 up until today. 

Using this dataset, we seek to study the evolution of agricultural practices and production around the world, their differences due to factors such as geographical predisposition, as well as emissions due to crops/cattle, food waste (i.e. crop residues), land use and energy. Our goal is to provide multiple exploratory visualizations, that would highlight the relationship between selected agricultural practices (crops, cattle, fertilizers, residue burning etc) and their total contributions to emissions, as well as their contribution to nutritional intake. We would like also to provide timelines on total production vs population growth in order to detect food waste and how to reduce it. 

Our final and optimistic goal is to use our results to try and analyze the approximate nutritional intake per capita from the current agricultural production, and extract the optimal agricultural strategy that would reduce emissions by a certain percentage, while enhancing the nutritional intake.

# Research questions: 

## Part 1: Exploration
- What is the overall impact of the agriculture industry on global green house gas (GHG) emissions ?
  - What are the sources of CH4 and N2O emissions from in the Agriculture Industry ?
  - How has the emissions global emissions of those gases from each source evolved in the past years ?
  - Which countries contribute the most to emissions due to agriculture ?
  - How has each country's COeq emissions evolved ? (Using a interactive map)
  
- How has the agriculture industry evolved in the time frame ?
  - What kind of crops/livestock increased in production in this time frame ?
  - Does overall production increase linearly with population ? Or did the food per person production increase ?
  - In detail: how has each item's (in Livestock and Crops) production evolved with respect to population ? And what are the differences ?
  - When and where fertilizer/pesticide started being used globally ?
  - How did fertilizer use change over time ?

## Part 2: Analysis
- What are the contributions of livestock/crops for each different emission type (enteric fermentation, etc ..) ?
- Have emissions increased proportionally to production ?
- Which product's production should be reduced as to reduce emissions ?
- How do livestock/crops production affect different emission types (enteric fermentation, etc ..) ?
- Which product's production should be reduced as to reduce pollution ?

## Part 3: Predictions
- What are the predictions for the future with the current model ?
- Do those changes affect the overall diet of the population ?
- How will emissions evolve in the future ?

# Dataset

We believe that we have found two versions of the same dataset: one found on Kaggle ( https://www.kaggle.com/unitednations/global-food-agriculture-statistics ), as well as one found directly on the UNFAO's website ( http://www.fao.org/faostat/en/#data ). The dataset found directly on the UNFAO's website is more up-to-date, and differently structured from the one on Kaggle -- it seems that latter is a cleaned and/or restructured version of the first. We would lean towards using the UNFAO's data directly as we believe that it is better to use data which is closer to its source. We will also note that our datasets contain interpolated values in order to cover gaps in data collection, which we might choose to drop.

The dataset contains 78 csv files, each representing different statistics related to Food and Agriculture, ranging from a few KiB to a couple of GiB of data. We believe we won't use all of them, as some describe numbers that are not needed such as Consumer prices, exchange rates food aid food balance, household surveys etc ...


This leaves us with 43 csv files, which have a very similar schema. It is a row based database, with each row having the following attributes (at least): 
`Area Code, Area, Item Code, Item, Element Code, Element, Year Code, Year, Unit, Value, Flag.`

The flag indicates the source of the data, and if it's estimated, computed, or raw measurements. Elements and element codes are a one to one relationship, and the same applies for Area Code and Area, Item and Item code. The unit is the unit of measurement. If the data is monthly, the column `Month` is added
# A list of internal milestones up until project milestone 2

1st milestone:

Data cleaning
- decide which csv files we are going to keep / trash by looking at the information they provide and the way it can be used to answer our main project inquiries
- with those remaining csv files, look at which values / variables can be removed; clean the remaining values and check whether all units are the same per element. Some units will need to be changed in order to analyze our results. 
- obtain yearly numbers per country (in data cleaning)
- make sure all units are relevant and understood: e.g. for some air pollutant emissions, make sure the units are relevant, evaluate how much CO2 and CH4 / other pollutants compare to each other.
- merge some csv into single dataframes in an effort to analyze separate variables jointly. Pivot the year variable in order to be able to analyze data from a time standpoint (as time series type values). Do the same thing with other variables in order to remove redundancies form the data set. At the momemt: each country each year each value has an entry... not efficient for analysis.
- also clean NaN values, remove / deal with values with specific associated flag values (flag is a variable which defines how / where the data comes from): flags for values that are inferred, etc...
- create a mapping in between variables and their associated variable codes (another variable): e.g. between element and element code, so we can do the analysis with the code (integers) and then go back to the element (descriptive string)


2nd milestone:

Data analysis:
- draw up a first draft of a way to quantify environmnental footprint: e.g. with pollutants production, fertilizer use, etc... Try different formulas to see which yield "correct" values and check with world rankings / other databases to see if it makes sense.
- if need be, add a variable-s which quantify environmental footprint/ crop efficiency, etc to be able to better compare countries and regions across the globes
- evaluate if year - to - year noise / variations are indicative of historical evolution and which are due to 'incorrect' values
- make sure that year to year values are relevant. Check if aberrant variations / values can be explained through historical context (e.g. big decrease in production because of war or hurricane / else). This could be in data analysis.
- see if some of our chosen variables are redundant when trying to answer the questions at hand
- see how to best aggregate variables and merge datasets for further analysis regarding environmental impact.
- output general visualization for chosen variables to start answering our main questions regarding environmental impact evolution (temporal and geographic evolution).

# Questions for TAs

- What are good libraries for geographical plots (i.e. maps) other than folium/bokeh ?
- Can we use external datasets for global emissions (all fields) and estimated nutritional value of crops for comparison ?
