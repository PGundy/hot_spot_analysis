
# Overview

An analytic reporting framework that removes any statitical ambiguity. This is achieved by taking an user provided function to calculate their metrics, running the function on combinations of user provided features, and then struturing the output into a tabular-ish data structure. 

The output data can be used to enhance reporting, find insights, and easily dive further into the 'why' metrics have shifted.

## Short Theoretical Demonstration:

If we have 3 columns [a, b, c], and we want to cut our data using those columns we would have to group our data as such to know all of the interactions' impact on our metric of interst. And this problem becomes increasingly complicated as we increase the number of columns. 

**Using 3 columns:**
[a, b, c] -> 7 valid data cuts
  - @ depth = 1: [a,b,c] <- 3 data cuts
  - @ depth = 2: [ab,ac,bc] <- 3 data cuts
  - @ depth = 3: [abc] <- 1 data cuts

***Note*** each column could have any number of valid values (ie rows when aggregated), thus 'ab' could be more accurately represented as a<sub>x</sub> * b<sub>y</sub> rows in the output. 


# An Example:

Using the titanic data from seaborn we can look at a semi-practical example using some data.

| survived | class | adult_male | embark_town |
| -------- | ----- | ---------- | ----------- |
| 0        | Third | True       | Southampton |
| 1        | First | False      | Cherbourg   |
| 1        | Third | False      | Southampton |
| 1        | First | False      | Southampton |
| 0        | Third | True       | Southampton |
*for each of the 891 passengers on the titanic*



## Basic hot_spot_analysis method:
```
import numpy as np
import pandas as pd
import seaborn as sb
from hot_spot_analysis.hot_spot_analysis import HotSpotAnalysis

# Load our data
df = sb.load_dataset('titanic')
titanic = df[['survived', 'class',  'adult_male', 'embark_town']]

# Define our metric function
def survival_rate(data):
    temp = data.agg(survived = pd.NamedAgg('survived', np.mean))
    return temp

# Input our data cuts, depth limit, and data
hsa = HotSpotAnalysis(
    data_cuts=['class',  'adult_male', 'embark_town'],
    depth_limit = 3,
    data = titanic
)

# Run the hot spot analysis
hsa.run_hsa(survival_rate)

# Export the data
hsa_output = hsa.get_hsa_data() # export the analysis results

# Review some of the features
print(hsa_output.head())
print(hsa_output.tail())

# Or use some of the built in search features
hsa.filter_hsa_data(
    target_var = 'data_content', 
    search_terms = 'Southampton'
    )


```

Using hot spot analysis we can get the following structure which scales exceptionally well as we increate the number of data cuts and interactions.

| depth | data_cuts        | data_content   | data_cut_content | output columns from user function |
| ----- | ---------------- | -------------- | ---------------- | --------------------------------- |
| 1     | [1 Column_Name]  | [1 row_value]  | [1 [column:row]] | [Int/float/etc.]                  |
| 2     | [2 Column_Names] | [2 row_values] | [2 [column:row]] | [Int/float/etc.]                  |
	


## Basic (mostly) pandas method

Does using hot_spot_analysis actually make life that much easier?
YES.

Looking at the following for 

```
import numpy as np
import pandas as pd
import seaborn as sb

df = sb.load_dataset('titanic')
titanic = df[['survived', 'class',  'adult_male', 'embark_town']]

def survival_rate(data):
    temp = data.agg(survived = pd.NamedAgg('survived', np.mean))
    return temp

titanic_by_class = survival_rate(titanic.groupby('class'))
titanic_by_adult_male = survival_rate(titanic.groupby('adult_male'))
titanic_by_embark_town = survival_rate(titanic.groupby('embark_town'))

# Then manually having to add the intersectionality of these features
titanic_by_embark_town = survival_rate(titanic.groupby(['class', 'adult_male', 'embark_town']))

## Even employing a loop these data objects do not align well to be joined and compare across groups.
print(titanic_by_embark_town)


# And now we have all the data, but in 7 dataframes with no clean key to combine.

```


