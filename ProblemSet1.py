#!/usr/bin/env python
# coding: utf-8

# # Excerise 0

# In[34]:


def github() -> str:
    """
    Returns a link to the solutions on GitHub
    """
    return "https://github.com/Ahuynh0519/PS/blob/main/ProblemSet1.py"


# In[36]:


print(github(Ahuynh0519, PS, "path/to/ProblemSet1.py"))


# # Excerise 1

# In[2]:


pip list


# # Excerise 2

# In[4]:


def evens_and_odds(n: int) -> dict:
    """
    Returns a dictionary with two keys, "evens" and "odds."
    "evens" is the sum of all even natural numbers less than n,
    and "odds" is the sum of all odd natural numbers less than n.
    """
    evens_sum = 0
    odds_sum = 0
    
    for i in range(1, n):
        if i % 2 == 0:
            evens_sum += i
        else:
            odds_sum += i
            
    return {"evens": evens_sum, "odds": odds_sum}
    
test_result = evens_and_odds(4)
test_result


# # Excerise 3 

# In[29]:


from typing import Union
from datetime import date 


# In[39]:


def time_diff(date_1: str, date_2: str, out: str) -> Union[str, int]:
    """
Calculates the absolute difference in days between two dates and returns the result
    either as a float value or a string message.
    
    Parameters:
    - date_1: str. The first date in 'YYYY-MM-DD' format.
    - date_2: str. The second date in 'YYYY-MM-DD' format.
    - out: str, optional. The format of the output: "float" for a numeric value,
      "string" for a textual description. Defaults to "float".
"""
    date_one = date.fromisoformat(date_1)
    date_two = date.fromisoformat(date_2)
    num_days = abs((date_two - date_one)).days  
    if out == 'string':
        return f'There are {num_days} days between the two dates'
    else:
        return num_days




# In[40]:


time_diff('2020-01-01','2020-01-02', 'float')


# In[41]:


time_diff('2020-01-03', '2020-01-01', 'string')


# # Excerise 4

# In[10]:


def reverse(in_list: list) -> list:
    reversed_list = []
    """
    Takes a list as an argument and returns a new list with the elements in reverse order.
    """
    for ele in range(len(in_list) - 1,-1, -1):  
        reversed_list.append(in_list[ele])  
        
    return reversed_list 


# In[11]:


reverse(['a','b','c'])


# # Excerise 5

# In[66]:


from math import factorial


# In[67]:


def prob_k_heads(n: int, k: int) -> float:
    """
    Calculate the probability of getting exactly k heads in n flips of a fair coin.

    :param n: Total number of flips
    :param k: Number of heads
    :return: Probability of getting k heads
    """
    # Binomial coefficient
    binom_coeff = factorial(n) / (factorial(k) * factorial(n - k))
    # Probability of getting k heads
    probability = binom_coeff * (0.5 ** k) * (0.5 ** (n - k))
    return probability
    


# In[68]:


print(prob_k_heads(1, 1))

