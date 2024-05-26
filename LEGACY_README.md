
# Overview
tldr: Do you hate trying to breakdown which underlying trends or movements are driving topline metric movements? HSA can solve that.

Hot Spot Analysis (HSA) is an analytic reporting framework that removes any statitical ambiguity. HSA is meant to enhance reporting, find insights, and easily dive further into the 'why' metrics have shifted. This is done by automatically running all viable cuts within the data across the provided features for any metrics.

## Future updates plan to add the following functionality:
- multiprocessing to improve module calculation speed
- support for non-dataframe user functions (graphs, etc.)


## Short Theoretical Demonstration:

If we have 3 columns [a, b, c], and we want to cut our data using those columns we would have to group our data as such to know all of the interactions' impact on our metric of interest. And this problem becomes increasingly complicated as we increase the number of columns. 

**Using 3 columns:**
[a, b, c] -> 7 valid data cuts
  - @ depth = 1: [a,b,c] <- 3 data cuts
  - @ depth = 2: [ab,ac,bc] <- 3 data cuts
  - @ depth = 3: [abc] <- 1 data cuts

**HSA Example Output Data Structure:**

| index | depth | data_cuts         | data_content        | data_cut_content      | user function output |
| ----- | ----- | ----------------- | ------------------- | --------------------- | -------------------- |
| 1     | 1     | [column a]        | [row_value x]       | ['a:x']               | [Int/float/etc.]     |
| 2     | 1     | [column b]        | [row_value y]       | ['b:y']               | [Int/float/etc.]     |
| 3     | 1     | [column c]        | [row_value z]       | ['c:z']               | [Int/float/etc.]     |
| 4     | 2     | [Columns a, b]    | [row_value x, y]    | ['a:x', 'b:y']        | [Int/float/etc.]     |
| 5     | 2     | [Columns a, c]    | [row_value x, z]    | ['a:x', 'c:z']        | [Int/float/etc.]     |
| 6     | 2     | [Columns b, c]    | [row_value y, z]    | ['b:y', 'c:z']        | [Int/float/etc.]     |
| 7     | 3     | [Columns a, b, c] | [row_value x, y, z] | ['a:x', 'b:y', 'c:z'] | [Int/float/etc.]     |

***Note:*** Each column yields X rows determined by the number of unique values. Thus 'ab' would yield a<sub>N</sub> * b<sub>M</sub> rows in the output where column a has N unique values, and column B has M unique values thus ab yields N*M rows.


# An Example:

Using the titanic data from seaborn we can look at a semi-practical example using some data.

| survived | class | adult_male | embark_town |
| -------- | ----- | ---------- | ----------- |
| 0        | Third | True       | Southampton |
| 1        | First | False      | Cherbourg   |
| 1        | First | False      | Southampton |
| 0        | Third | True       | Queenstown  |
*for each of the 891 passengers on the titanic*



## A Simple Example Using hot_spot_analysis:
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
    temp = data.agg(survival_rate = pd.NamedAgg('survived', np.mean))
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
hsa.search_hsa_data(
    target_var = 'data_content', 
    search_terms = 'Southampton'
    )

```


## A (mostly) pandas example without hot_spot_analysis:

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
    temp = data.agg(survival_rate = pd.NamedAgg('survived', np.mean))
    return temp

titanic_by_class = survival_rate(titanic.groupby('class'))
titanic_by_adult_male = survival_rate(titanic.groupby('adult_male'))
titanic_by_embark_town = survival_rate(titanic.groupby('embark_town'))
titanic_by_class_adult_male = survival_rate(titanic.groupby(['class', 'adult_male']))
titanic_by_class_embark_town = survival_rate(titanic.groupby(['class', 'embark_town']))
titanic_by_adult_male_embark_town = survival_rate(titanic.groupby(['adult_male', 'embark_town']))
titanic_by_all = survival_rate(titanic.groupby(['class', 'adult_male', 'embark_town']))

# Combine the data frames
dfs = [
    titanic_by_class,
    titanic_by_adult_male,
    titanic_by_embark_town,
    titanic_by_class_adult_male,
    titanic_by_class_embark_town,
    titanic_by_adult_male_embark_town,
    titanic_by_all
]

all_df = pd.concat(dfs, join='outer', axis=1).fillna(np.NaN)

# Review some of the features
print(all_df.head())
print(all_df.tail())



```


