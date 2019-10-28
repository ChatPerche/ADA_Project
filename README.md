# Title 
Environmental Impact of Agricultural Practices in the World. 

# Abstract
The FAOSTAT dataset provides country-based data of agricultural production, imports and exports over the years, starting in 1961. This dataset also contains metrics such as air pollutant emission, fertilizer and pesticide use, forest cover, etc... 
We seek to study the environmental impact of different agricultural practices and compare countries through this lens. We hope to identify best practices in terms of environmental impact. For example, we would like to visualize quantities of various air pollutant emissions according to different crops and livestock in order to investigate which products have the highest nutritional values and lowest environmental impacts. We would also like to study which countries are best able to maximize production while minimizing environmental impact. 
The dataset is very rich and there are multiple angles of attack here; we can look at problem from an economic point of view ( there is information on local agricultural markets in the dataset ) or a nutritional one ( by looking at the nutrients in each crop ). We could even go so far as to study which agricultural subsidies could best serve both nutritional and environmental values for given countries. 

# Research questions: 

- How to structure the data for analysis ?
- Some values are not official and are approximations. What should we do with those numbers ?
- How can we estimate the true emissions of a certain product, independant of the yield, surface area of crops and type of fertilizer used?
- How will we associate nutritional value of products and relate them to the emissions for cultivation ?
- How to eliminate the bias of different climates in order to compare different yields when different fertilizers are used ?

# Dataset

We believe that we have found two versions of the same dataset: one found on Kaggle ( https://www.kaggle.com/unitednations/global-food-agriculture-statistics ), as well as one found directly on the UNFAO's website ( http://www.fao.org/faostat/en/#data ). The dataset found directly on the UNFAO's website is more up-to-date, and differently structured from the one on Kaggle -- it seems that latter is a cleaned and/or restructured version of the first. We would lean towards using the UNFAO's data directly as we believe that it is better to use data which is closer to its source. We will also note that our datasets contain interpolated values in order to cover gaps in data collection, which we might choose to drop.  

# A list of internal milestones up until project milestone 2

- Load and study the data. More clearly define our objectives according to the exploitability of the data. 
- Restructure and clean the data to have them in the format which could best serve our objectives

# Questions for TAa

- How do we decide which data to keep / discard ( based on where it comes from / flags, years ... ) ?
- How do we quantify environmental footprint accurately enough based on the information at hand ( e.g. fertilizers, agricultural land, etc...) ?
- How do we evaluate the data evolution with respect to time? There is noise from year-to-year, and for longer periods of time there are inconsistencies in product definitions (per FOA website), and there are some events (wars, embargos, etc...) which might have a storng impact on dataset values, at least country-wise.
