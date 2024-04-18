#!/usr/bin/env python
# coding: utf-8

# # Exercise 0

# In[3]:


def github() -> str:
    """
    Returns a link to the solutions on GitHub
    """
    return "https://github.com/Ahuynh0519/EconPS/blob/main/ProblemSet3.py"


# In[4]:


pip list


# In[ ]:


# Exercise 1


# In[42]:


import pandas as pd

file_path1 = f'/mnt/data/ghgp_data_2019.xlsx'
file_path2 = f'/mnt/data/ghgp_data_2020.xlsx'
file_path3 = f'/mnt/data/ghgp_data_2021.xlsx'
file_path4 = f'/mnt/data/ghgp_data_2022.xlsx'
years = [""] * 4
years[0] = file_path1
years[1] = file_path2
years[2] = file_path3
years[3] = file_path4

def import_yearly_data(years: list) -> pd.DataFrame:
    """
    Imports yearly data for direct emitters from the EPA's Excel sheets for the specified years.

    Args:
        years (list): A list of integers where each integer represents a year for which the data is to be imported.

    Returns:
        pd.DataFrame: A concatenated DataFrame containing data from all specified years.
    """
   
    data_frames = pd.DataFrame()
    
    for i in range(len(years)):
       
        file_path = years[i]
        
        df = pd.read_excel(file_path, sheet_name='Direct Emitters', header=3, skiprows=range(3))

        reversed_path = file_path[::-1]
        reversed_path = reversed_path[5:9]
        reveresed_path = reversed_path[::-1]
        df['year'] = reversed_path
        
     
        data_frames.append(df)


    concatenated_data = pd.concat(data_frames, ignore_index=True)
    
    return concatenated_data


# # Exercise 2

# In[43]:


import pandas as pd

def import_parent_companies(years: list) -> pd.DataFrame:
    """
    This function takes a list of years, reads the Excel sheet for parent companies data for each year,
    and concatenates these DataFrames into a single DataFrame. The function assumes that the Excel files
    are in the .xlsb format. It adds a 'year' column to each DataFrame indicating the year of data,
    and it removes rows that are entirely null.

    Parameters:
    years (list): A list of integers representing the years for which the data should be loaded.

    Returns:
    pd.DataFrame: A concatenated DataFrame containing data from all specified years with rows that are
    entirely null removed.
    """
   
    data_frames = []

    for year in years:
        
        file_path = f'/mnt/data/ghgp_data_parent_company_09_2023.xlsb'
        
        
        df = pd.read_excel(file_path, sheet_name='Sheet1', engine='pyxlsb', header=0)
 
        df['year'] = year
        
       
        df = df.dropna(how='all')
        
        
        data_frames.append(df)
    
    concatenated_df = pd.concat(data_frames, ignore_index=True)
    
    return concatenated_df




# # Exercise 3

# In[6]:


get_ipython().system('pip install pyxlsb')


# In[40]:


import pandas as pd

def n_null(df: pd.DataFrame, col: str) -> int:
    """
    Counts the number of null (NaN) values in a specified column of a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        col (str): The column name in the DataFrame where null values are to be counted.

    Returns:
        int: The number of null values in the specified column.
    """
   
    null_count = df[col].isnull().sum()
    return null_count


# In[41]:


df = pd.DataFrame({
 'A': [1, 2, None, 4],
 'B': ['x', None, 'y', 'z']
 })
 
print(n_null(df, 'A'))  
print(n_null(df, 'B'))  


# # Exercise 4

# In[31]:


import pandas as pd

def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:
    """
    Performs data cleaning and merging on emissions and parent company data. The function executes a left join
    using 'year' and 'Facility ID' as join keys. It then subsets the data to include specified variables
    and converts all column names to lower case.

    Parameters:
    emissions_data (pd.DataFrame): A DataFrame containing emissions data.
    parent_data (pd.DataFrame): A DataFrame containing parent company data.

    Returns:
    pd.DataFrame: A cleaned and merged DataFrame with specified columns in lower-case.
    """
   
    merged_data = pd.merge(emissions_data, parent_data,
                           how='left',
                           left_on=['year', 'Facility ID'],
                           right_on=['year', 'Facility ID'])

   
    selected_columns = [
        'Facility ID',
        'year',
        'State',
        'Industry Type (sectors)',
        'Total reported direct emissions',
        'PARENT CO. STATE',
        'PARENT CO. PERCENT OWNERSHIP'
    ]
    

    final_data = merged_data[[col for col in selected_columns if col in merged_data.columns]]

    final_data.columns = [col.lower() for col in final_data.columns]

    return final_data

emissions_df = pd.DataFrame({
    'year': [2020, 2020],
     'Facility ID': [1, 2],
     'State': ['TX', 'CA'],
    'Industry Type (sectors)': ['Manufacturing', 'Power'],
     'Total reported direct emissions': [1000, 2000]})
 
parent_df = pd.DataFrame({
     'year': [2020, 2020],
     'Facility ID': [1, 2],
     'PARENT CO. STATE': ['TX', 'CA'],
     'PARENT CO. PERCENT OWNERSHIP': [100, 90] })
cleaned_df = clean_data(emissions_df, parent_df)
print(cleaned_df)


# # Exercise 5

# In[35]:


import pandas as pd

def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    """
    Aggregates the DataFrame by specified group variables and calculates the minimum, median,
    mean, and maximum values for 'total reported direct emissions' and 'parent co. percent ownership'.
    The resulting DataFrame is sorted by the mean of 'total reported direct emissions' in descending order.

    Parameters:
    df (pd.DataFrame): A DataFrame with emissions and parent company information.
    group_vars (list of str): Variables on which to group the data.

    Returns:
    pd.DataFrame: Aggregated and sorted DataFrame with calculated statistics.
    """
    
    agg_functions = {
        'total reported direct emissions': ['min', 'median', 'mean', 'max'],
        'parent co. percent ownership': ['min', 'median', 'mean', 'max']
    }

   
    aggregated_df = df.groupby(group_vars).agg(agg_functions)

    
    aggregated_df.columns = ['_'.join(col).strip() for col in aggregated_df.columns.values]

    
    sorted_df = aggregated_df.sort_values(by='total reported direct emissions_mean', ascending=False)

    return sorted_df


# Define a sample DataFrame according to the schema from Exercise 4
sample_df = pd.DataFrame({
     'state': ['TX', 'TX', 'CA', 'CA'],
     'total reported direct emissions': [1000, 2000, 500, 1500],
     'parent co. percent ownership': [100, 90, 85, 75]
 })
result = aggregate_emissions(sample_df, ['state'])
print(result)


# In[ ]:




