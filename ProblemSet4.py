#!/usr/bin/env python
# coding: utf-8

# # Problem Set 4

# # Excerise 0

# In[1]:


def github() -> str:
    """
    Returns a link to the solutions on GitHub
    """
    return "https://github.com/Ahuynh0519/EconPS/blob/main/ProblemSet4.py"



# In[4]:


pip list


# # Exercise 1

# In[13]:


import os
print(os.getcwd())


# In[14]:


print(os.listdir())


# In[2]:


import pandas as pd

def load_data() -> pd.DataFrame:
    """
    Load Tesla stock price history from a CSV file and return it as a pandas DataFrame.
    
    Returns:
    pd.DataFrame: DataFrame containing Tesla stock price data.
    """
    
    file_path = 'TSLA.csv'  
    data = pd.read_csv(file_path)
    return data


# # Exercise 2

# In[3]:


import pandas as pd
import matplotlib.pyplot as plt

def plot_close(df: pd.DataFrame, start: str = '2010-06-29', end: str = '2024-04-15') -> None:
    """
    Plot the closing prices of Tesla stock within a specified date range.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing Tesla stock price data.
    start (str): Start date for the plot, formatted as 'YYYY-MM-DD'.
    end (str): End date for the plot, formatted as 'YYYY-MM-DD'.
    """
    
    mask = (df['Date'] >= start) & (df['Date'] <= end)
    filtered_data = df.loc[mask]

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_data['Date'], filtered_data['Close'], label='Closing Price', color='blue')
    plt.title(f'Tesla Closing Stock Prices from {start} to {end}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price ($)')
    plt.grid(True)
    plt.xticks(rotation=45)  
    plt.legend()
    plt.tight_layout()
    plt.show()


data = load_data()
plot_close(data)  


# # Exercise 3

# In[4]:


df = pd.read_csv('TSLA.csv')  


# In[5]:


import pandas as pd
import statsmodels.api as sm

def autoregress(df: pd.DataFrame) -> float:
    """
    Perform an autoregression on the closing prices of a stock and return the t-statistic
    for the slope coefficient without an intercept, using HC1 standard errors.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing the closing prices of a stock.

    Returns:
    float: The t-statistic for the slope coefficient from the regression.
    """
    
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df['Delta_Close'] = df['Close'].diff()
    df = df.dropna()

    
    X = df['Delta_Close'].iloc[:-1].values

    y = df['Delta_Close'].iloc[1:].values

    
    model = sm.OLS(y, X, hasconst=False)
    results = model.fit(cov_type='HC1')  

    
    return results.tvalues[0]


t_statistic = autoregress(df)
t_statistic


# # Exercise 4

# In[6]:


import pandas as pd
import numpy as np
from statsmodels.discrete.discrete_model import Logit

# Reload the data
df = pd.read_csv('TSLA.csv')

def autoregress_logit(df: pd.DataFrame) -> float:
    """
    Performs a logistic regression on the closing prices of Tesla's stock, specifically on the
    lagged changes in the closing prices, and returns the t-statistic for the coefficient
    from the logistic regression.

    Parameters:
    df (pd.DataFrame): DataFrame containing the closing prices of Tesla's stock.

    Returns:
    float: The t-statistic for the slope coefficient from the logistic regression.
    """
    
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df['Delta_Close'] = df['Close'].diff()
    df['Positive_Change'] = (df['Delta_Close'] > 0).astype(int)
    df['Lagged_Delta_Close'] = df['Delta_Close'].shift(1)
    df.dropna(inplace=True)

 
    X = df[['Lagged_Delta_Close']]

   
    y = df['Positive_Change']

    
    model = Logit(y, X)
    results = model.fit(disp=0)  

    
    return results.tvalues['Lagged_Delta_Close']


t_statistic_logit = autoregress_logit(df)
t_statistic_logit


# # Exercise 5

# In[7]:


import matplotlib.pyplot as plt

def plot_delta(df: pd.DataFrame) -> None:
    """
    Plots the daily change in the closing price (Delta_Close) for the given DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame containing Tesla stock price data.
    """
    # Calculate the change in closing price from the previous day
    df['Delta_Close'] = df['Close'].diff()

    # Plot the Delta_Close
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Delta_Close'], label='Daily Change in Closing Price')
    plt.xlabel('Date')
    plt.ylabel('Change in Closing Price ($)')
    plt.title('Daily Change in Tesla Closing Price')
    plt.legend()
    plt.grid(True)
    plt.show()
    
plot_delta(df)

