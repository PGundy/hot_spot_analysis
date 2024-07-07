# hot-spot-analysis

A brief description of your package.

## Installation

```zsh
pip install hot-spot-analysis
```

## Python Import
```python
from hot_spot_analysis.hot_spot_analysis import HotSpotAnalyzer
HSA = HotSpotAnalyzer(...)
```

# Quickstart 

## Short Theoretical Demonstration:
If we have 3 columns [a, b, c], and we want to cut our data using those columns we would have to group our data as such to know all of the interactions' impact on our metric of interest. And this problem becomes increasingly complicated as we increase the number of columns. 

**Interacting 3 columns:**
[a, b, c] -> 7 valid data cuts
  - @ depth = 1: [a,b,c] <- 3 data cuts
  - @ depth = 2: [ab,ac,bc] <- 3 data cuts
  - @ depth = 3: [abc] <- 1 data cuts

## A simple example of Hot Spot Analysis (HSA)

### Example - Input Data
| column1 | column2 | Value |
| ------- | ------- | ----- |
| A       | X       | 10    |
| A       | Y       | 20    |
| B       | X       | 30    |
| B       | Y       | 40    |
| C       | X       | 50    |
| C       | Y       | 60    |

### Example - Simple metric function
```python
# Metric function
def metric_function(group):
    return {
        'sum_value': group['Value'].sum()
    }
```

### Example Run HSA
```python
from hot_spot_analysis.hot_spot_analysis import HotSpotAnalyzer

HSA = HotSpotAnalyzer(
    data=example_data,                  # See above
    target_cols=["column1", "column2"], 
    objective_function=metric_function, # See above
)

HSA.run_hsa()
hsa_data = HSA.export_hsa_output_df()
print(hsa_data.head(10))
```

**Below is a simplified example of the HSA output**

| group                            | n_rows | sum_value |
| -------------------------------- | ------ | --------- |
| {'column1': 'A'}                 | 2      | 30        |
| {'column1': 'B'}                 | 2      | 70        |
| {'column1': 'C'}                 | 2      | 110       |
| {'column2': 'X'}                 | 3      | 90        |
| {'column2': 'Y'}                 | 3      | 120       |
| {'column1': 'A', 'column2': 'X'} | 1      | 10        |
| {'column1': 'A', 'column2': 'Y'} | 1      | 20        |
| {'column1': 'B', 'column2': 'X'} | 1      | 30        |
| {'column1': 'B', 'column2': 'Y'} | 1      | 40        |
| {'column1': 'C', 'column2': 'X'} | 1      | 50        |
| {'column1': 'C', 'column2': 'Y'} | 1      | 60        |