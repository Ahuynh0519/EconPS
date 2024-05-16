#!/usr/bin/env python
# coding: utf-8

# # Problem Set 6

# # Excerise 0

# In[41]:


def github() -> str:
    """
    Returns a link to the solutions on GitHub
    """
    return "https://github.com/Ahuynh0519/EconPS/blob/main/ProblemSet6.py"


# # Excerise 1

# In[32]:


def std() -> str:
    """
    Returns a SQL query that outputs a table with two columns:
    itemId: the ID of the item
    std: the unbiased standard deviation of bids for that item, considering only items with at least two bids.
    """
    query = """
    WITH bid_counts AS (
        SELECT 
            itemId,
            COUNT(bidAmount) AS bid_count
        FROM bids
        GROUP BY itemId
    ),
    item_means AS (
        SELECT 
            itemId,
            AVG(bidAmount) AS mean_bid
        FROM bids
        GROUP BY itemId
    ),
    squared_diffs AS (
        SELECT 
            b.itemId,
            (b.bidAmount - im.mean_bid) * (b.bidAmount - im.mean_bid) AS squared_diff
        FROM bids b
        JOIN item_means im ON b.itemId = im.itemId
    ),
    variances AS (
        SELECT 
            sd.itemId,
            SUM(sd.squared_diff) / (bc.bid_count - 1) AS variance
        FROM squared_diffs sd
        JOIN bid_counts bc ON sd.itemId = bc.itemId
        WHERE bc.bid_count >= 2
        GROUP BY sd.itemId
    )
    SELECT 
        v.itemId,
        SQRT(v.variance) AS std
    FROM variances v;
    """
    return query


# In[33]:


import sqlite3
import os


db_path = 'auctions.db'  
if os.path.exists(db_path):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    
    query = std()
    
    
    result = cursor.execute(query).fetchall()
    for row in result:
        print(row)

    
    conn.close()
else:
    print(f"The database file at {db_path} does not exist.")


# # Exercise 2

# In[34]:


def bidder_spend_frac() -> str:
    """
    Returns a SQL query that outputs a table with four columns:
    bidderName: the name of the bidder
    total_spend: the amount the bidder spent (the sum of their winning bids)
    total_bids: the amount the bidder bid, considering only the highest bid per item
    spend_frac: total_spend/total_bids
    """
    query = """
    WITH highest_bids AS (
        SELECT 
            bidderName, 
            itemId, 
            MAX(bidAmount) AS highest_bid
        FROM bids
        GROUP BY bidderName, itemId
    ),
    winning_bids AS (
        SELECT 
            highBidderName AS bidderName, 
            SUM(bidAmount) AS total_spend
        FROM bids
        WHERE isBuyerHighBidder = 1
        GROUP BY highBidderName
    ),
    total_bids AS (
        SELECT 
            bidderName, 
            SUM(highest_bid) AS total_bids
        FROM highest_bids
        GROUP BY bidderName
    )
    SELECT 
        t1.bidderName,
        t2.total_spend,
        t1.total_bids,
        t2.total_spend * 1.0 / t1.total_bids AS spend_frac
    FROM total_bids t1
    LEFT JOIN winning_bids t2 ON t1.bidderName = t2.bidderName;
    """
    return query


# In[36]:


import sqlite3


db_path = 'auctions.db'  
if os.path.exists(db_path):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

  
    query = bidder_spend_frac()
    
    
    result = cursor.execute(query).fetchall()
    for row in result:
        print(row)

    
    conn.close()
else:
    print(f"The database file at {db_path} does not exist.")


# # Exercise 3

# In[37]:


import os
import sqlite3


db_path = 'auctions.db'
if os.path.exists(db_path):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    def min_increment_freq() -> str:
        """
        Returns a SQL query that outputs a table with one column (freq) representing the fraction of bids 
        in the database that are exactly the minimum bid increment (items.bidIncrement) above the previous 
        high bid, excluding items where isBuyNowUsed=1.
        """
        query = """
        WITH previous_bids AS (
            SELECT 
                b1.itemId, 
                b1.bidAmount AS current_bid,
                b2.bidAmount AS previous_bid,
                i.bidIncrement
            FROM bids b1
            JOIN items i ON b1.itemId = i.itemId
            LEFT JOIN bids b2 ON b1.itemId = b2.itemId AND b2.bidTime < b1.bidTime
            WHERE i.isBuyNowUsed = 0
        ),
        valid_bids AS (
            SELECT 
                itemId, 
                COUNT(*) AS total_bids,
                SUM(CASE WHEN current_bid = previous_bid + bidIncrement THEN 1 ELSE 0 END) AS increment_bids
            FROM previous_bids
            GROUP BY itemId
        )
        SELECT 
            SUM(increment_bids) * 1.0 / SUM(total_bids) AS freq
        FROM valid_bids;
        """
        return query

   
    query = min_increment_freq()
    result = cursor.execute(query).fetchall()
    print(result)

   
    conn.close()
else:
    print(f"The database file at {db_path} does not exist.")


# # Exercise 4

# In[38]:


def win_perc_by_timestamp() -> str:
    """
    Returns a SQL query that outputs a table with two columns:
    timestamp_bin: The bin corresponding to the normalized percentage of time remaining in the auction when a bid is placed.
    win_perc: The frequency with which a bid placed with this timestamp bin won the auction.
    """
    query = """
    WITH normalized_bids AS (
        SELECT 
            b1.bidLogId,
            b1.itemId,
            b1.bidderName,
            b1.bidTime,
            (JULIANDAY(b1.bidTime) - JULIANDAY(i.startTime)) / (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) AS norm_time,
            CASE 
                WHEN (JULIANDAY(b1.bidTime) - JULIANDAY(i.startTime)) / (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) <= 0.1 THEN 1
                WHEN (JULIANDAY(b1.bidTime) - JULIANDAY(i.startTime)) / (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) <= 0.2 THEN 2
                WHEN (JULIANDAY(b1.bidTime) - JULIANDAY(i.startTime)) / (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) <= 0.3 THEN 3
                WHEN (JULIANDAY(b1.bidTime) - JULIANDAY(i.startTime)) / (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) <= 0.4 THEN 4
                WHEN (JULIANDAY(b1.bidTime) - JULIANDAY(i.startTime)) / (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) <= 0.5 THEN 5
                WHEN (JULIANDAY(b1.bidTime) - JULIANDAY(i.startTime)) / (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) <= 0.6 THEN 6
                WHEN (JULIANDAY(b1.bidTime) - JULIANDAY(i.startTime)) / (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) <= 0.7 THEN 7
                WHEN (JULIANDAY(b1.bidTime) - JULIANDAY(i.startTime)) / (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) <= 0.8 THEN 8
                WHEN (JULIANDAY(b1.bidTime) - JULIANDAY(i.startTime)) / (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) <= 0.9 THEN 9
                ELSE 10
            END AS timestamp_bin
        FROM bids b1
        JOIN items i ON b1.itemId = i.itemId
    ),
    winning_bids AS (
        SELECT 
            bidLogId,
            1 AS is_winner
        FROM bids
        WHERE isBuyerHighBidder = 1
    )
    SELECT 
        timestamp_bin,
        SUM(is_winner) * 1.0 / COUNT(*) AS win_perc
    FROM normalized_bids
    LEFT JOIN winning_bids USING(bidLogId)
    GROUP BY timestamp_bin
    ORDER BY timestamp_bin;
    """
    return query


# In[39]:


import sqlite3
import os


db_path = 'auctions.db'  
if os.path.exists(db_path):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    
    query = win_perc_by_timestamp()
    
   
    result = cursor.execute(query).fetchall()
    for row in result:
        print(row)

    
    conn.close()
else:
    print(f"The database file at {db_path} does not exist.")

