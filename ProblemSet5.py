#!/usr/bin/env python
# coding: utf-8

# # Problem Set 5

# # Exercise 0

# In[2]:


def github() -> str:
    """
    Returns a link to the solutions on GitHub
    """
    return "https://github.com/Ahuynh0519/EconPS/blob/main/ProblemSet5.py"


# # Exercise 1

# In[11]:


pip install requests


# In[2]:


import requests

def fetch_webpage(url):

    response = requests.get(url)

    
    if response.status_code == 200:
        print("Success! Webpage fetched successfully.")
        return response.text  # Return the content of the webpage
    else:
        print("Failed to fetch the webpage.")
        return None


url = "https://lukashager.netlify.app/econ-481/01_intro_to_python"
webpage_content = fetch_webpage(url)

if webpage_content:
    print("Webpage content:")
    print(webpage_content[:500])  
else:
    print("No content to display.")


# In[ ]:


import requests
from bs4 import BeautifulSoup

def scrape_code(url: str) -> str:
    """
    Fetches the webpage at the provided URL and extracts Python code blocks, omitting any IPython magic commands.
    The extracted code is returned as a single string, suitable for saving as a Python script, assuming that
    the code is syntactically correct (ignoring intentional syntax errors in the lecture content).

    Returns:
    
        str: A single string containing all Python code blocks from the webpage, formatted for execution.
    """
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')

    
    all_code = ""

    
    for code in soup.find_all('code'):
      
        code_text = code.get_text()


        filtered_code = '\n'.join(line for line in code_text.splitlines() if not line.strip().startswith('%'))
        
        
        if filtered_code:
            all_code += filtered_code + '\n\n'

    return all_code.strip()  


