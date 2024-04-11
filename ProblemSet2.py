#!/usr/bin/env python
# coding: utf-8

# # Exercise 0 

# In[1]:


def github() -> str:
    """
    Returns a link to the solutions on GitHub
    """
    return "https://github.com/Ahuynh0519/EconPS/blob/main/ProblemSet2.py"


# # Exercise 1

# In[10]:


import numpy as np

def simulate_data(seed: int = 481) -> tuple:
    """
    Simulate data for a linear model with three predictors.
    Each predictor and the error term are drawn from a normal distribution.
    The model is: y = 5 + 3*x1 + 2*x2 + 6*x3 + ε

    Parameters:
    seed (int): The seed for the random number generator, defaults to 481.

    Returns:
    tuple: A tuple containing the response vector y and the predictor matrix X.
           y is a 1000x1 np.array, X is a 1000x3 np.array.
    """
    np.random.seed(seed)  # Set the seed for reproducibility
    
    # Parameters for the simulation
    n = 1000  # Number of observations
    β = np.array([5, 3, 2, 6])  # Model coefficients including intercept
    σ_x = 2  # Standard deviation for x variables
    σ_ε = 1  # Standard deviation for the error term
    
    
    X = np.random.normal(0, σ_x, size=(n, 3))
    
    
    ε = np.random.normal(0, σ_ε, size=n)
    
    X_with_intercept = np.hstack((np.ones((n, 1)), X))
    
    y = X_with_intercept.dot(β) + ε
    
    return y, X



# In[11]:


y, X = simulate_data()


# # Exercise 2

# In[12]:


import numpy as np
from scipy.optimize import minimize

def estimate_mle(y: np.array, X: np.array) -> np.array:
    """
    Estimates the MLE parameters for a linear regression model.

    Parameters:
    y (np.array): A 1000 x 1 np.array of the response variable.
    X (np.array): A 1000 x 3 np.array of the predictor variables.

    Returns:
    np.array: A 4 x 1 np.array with the coefficients β0, β1, β2, β3.
    """
    
    X_with_intercept = np.hstack((np.ones((X.shape[0], 1)), X))
    
    
    def neg_log_likelihood(beta):
        residuals = y - X_with_intercept.dot(beta)
        ssr = np.sum(residuals**2)
        
        return 0.5 * ssr
    
   
    initial_beta = np.zeros(X_with_intercept.shape[1])
    
   
    result = minimize(neg_log_likelihood, initial_beta, method='BFGS')
    
    
    beta_mle = result.x

    return beta_mle.reshape(-1, 1)



# # Exercise 3

# In[13]:


import numpy as np

def estimate_ols(y: np.array, X: np.array) -> np.array:
    """
    Estimates the OLS coefficients for a linear regression model using the closed-form solution.

    Parameters:
    y (np.array): A 1000 x 1 np.array of the response variable.
    X (np.array): A 1000 x 3 np.array of the predictor variables.

    Returns:
    np.array: A 4 x 1 np.array with the coefficients β0, β1, β2, β3 (in that order).
    """
   
    X_with_intercept = np.hstack((np.ones((X.shape[0], 1)), X))
    
    
    beta_hat = np.linalg.inv(X_with_intercept.T @ X_with_intercept) @ X_with_intercept.T @ y
    
    return beta_hat



