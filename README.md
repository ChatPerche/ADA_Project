# Title 
Environmental Impact of Agricultural Practices in the World. 

# Abstract

The FAOSTAT dataset provides agricultural production, import and export data for over 245 countries starting in 1961, as well metrics such as emissions, fertilization use, pesticide use, forest coverage etc. We seek to study the impact of different agricultural practices on the environment, and to compare countries through this lens. Our hope is to identify best practices. For example, we would like to visualize different emissions according to different crops and/or livestock, in order to study which products have the highest nutritional values and lowest environmental impacts. We would also like to study which countries are able to maximize production whilst minimizing environmental impact. The dataset is very rich and there are multiple angles of attack here : we can look at problem from an economic point of view ( as we have information on local agricultural markets ) or a nutritional one ( by looking at the nutrients in each crop ). We could, for example, go so far as to study which agricultural subsidies could best serve both nutritional and environmental values. 

# Research questions: 

- How to structure the data for our analysis ?
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

- How do we decide which data to keep / trash based on where it comes from / flags, years ...
- How do we more or less accurately quantify environmental footprint based on the information at hand? e.g. fertilizers, agricultural land, etc...
- How do we evaluate the data evolution with respect to time? Noise year-to-year, but for longer periods of time: inconsistencies in product definitions, etc... (per FOA website)
Add here some questions you have for us, in general or project-specific.
