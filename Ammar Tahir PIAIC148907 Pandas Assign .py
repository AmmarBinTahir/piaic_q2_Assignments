#!/usr/bin/env python
# coding: utf-8

# In[36]:


#PART 1:

#HOW TO CLEAN DATA WITH PYTHON Cleaning US Census Data.
#You just got hired as a Data Analyst at the Census Bureau, which collects census data and creates interesting visualizations and insights from it.
# The person who had your job before you left you all the data they had for the most recent census. 
#It is in multiple csv files. They didn’t use pandas, they would just look through these csv files manually whenever they wanted to find something. Sometimes they would copy and paste certain numbers into Excel to make charts.
#The thought of it makes you shiver. This is not scalable or repeatable.
#Your boss wants you to make some scatterplots and histograms by the end of the day. Can you get this data into pandas and into reasonable shape so that you can make these histograms?
#Inspect the Data! 1. 
#The first visualization your boss wants you to make is a scatterplot that shows average income in a state vs proportion of women in that state.
#Open some of the census csv files in the navigator. How are they named? What kind of information do they hold? 
#Will they help us make this graph?

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from glob import glob


# In[53]:



#It will be easier to inspect this data once we have it in a DataFrame. 
#You can’t even call .head() on these csvs! How are you supposed to read them?
#Using glob, loop through the census files available and load them into DataFrames. 
#Then, concatenate all of those DataFrames together into one DataFrame, called something like us_census.

files = glob("states*")
files


# In[5]:


us_census = pd.concat((pd.read_csv(file) for file in files ),ignore_index=True)
us_census.head()


# In[6]:


#3. Look at the .columns and the .dtypes of the us_census DataFrame. 
#Are those datatypes going to hinder you as you try to make histograms?

us_census.columns


# In[13]:


# 4. Look at the .head() of the DataFrame so that you can understand why some of these dtypes are objects instead of integers or floats.

#Start to make a plan for how to convert these columns into the right types for manipulation.

us_census.head()


# In[17]:


# 5. Use regex to turn the Income column into a format that is ready for conversion into a numerical type.


us_census.dtypes


# In[30]:


# 6. Look at the GenderPop column. 
# We are going to want to separate this into two columns, the Men column, and the Women column.
# Split the column into those two new columns using str.split and separating out those results.

us_census[["the Men","the Women"]] = us_census["GenderPop"].str.split("_",expand = True)

us_census.head()


# In[31]:


us_census["the Men"] = us_census["the Men"].str.replace("M","")
us_census["the Men"] = pd.to_numeric(us_census["the Men"])


# In[32]:


us_census["the Women"] = us_census["the Women"].str.replace("F","")
us_census["the Women"] = pd.to_numeric(us_census["the Women"])


# In[33]:


#. Now you should have the columns you need to make the graph and make sure your boss does not slam a ruler angrily on your desk because you’ve wasted your whole day cleaning your data with no results to show!

# Use matplotlib to make a scatterplot!

#plt.scatter(the_women_column, the_income_column) Remember to call plt.show() to see the graph!

plt.scatter(us_census["the Women"], us_census["Income"])
plt.show()


# In[34]:


# 9. Did you get an error? These monstrous csv files probably have nan values in them! 
# Print out your column with the number of women per state to see.

# We can fill in those nans by using pandas’ .fillna() function.

# You have the TotalPop per state, and you have the Men per state. As an estimate for the nan values in the Women column, you could use the TotalPop of that state minus the Men for that state.

# Print out the Women column after filling the nan values to see if it worked!

us_census["the Women"] = us_census["the Women"].fillna(us_census["TotalPop"]-us_census["the Men"]).astype(int)


# In[35]:


# 10. We forgot to check for duplicates! Use .duplicated() on your census DataFrame to see if we have duplicate rows in there.
us_census.duplicated()


# In[38]:


#11. Drop those duplicates using the .drop_duplicates() function.

us_census.drop_duplicates(inplace = True)


# In[39]:


#12.Make the scatterplot again. Now, it should be perfect! Your job is secure, for now.
plt.scatter(us_census["the Women"], us_census["Income"])
plt.show()


# In[50]:


#13. Now, your boss wants you to make a bunch of histograms out of the race data that you have.
#Look at the .columns again to see what the race categories are.

us_census.columns


# In[51]:


#14. Try to make a histogram for each one!

# You will have to get the columns into numerical format, and those percentage signs will have to go.

# Don’t forget to fill the nan values with something that makes sense!
#You probably dropped the duplicate rows when making your last graph, but it couldn’t hurt to check for duplicates again.


# In[54]:


def fill(Name):
  us_census[Name] = us_census[Name].fillna(us_census[Name].mean())
fill("Pacific")


# In[55]:


us_census.duplicated()


# In[56]:


x = ["Hispanic","White","Black","Native","Asian","Pacific"]
plt.hist(x,bins=10)


# In[57]:


#Part2
#1. Data for all of the locations of Petal Power is in the file inventory.csv. Load the data into a DataFrame called inventory.


inventory = pd.read_csv("inventory.csv")


# In[58]:


#2. Inspect the first 10 rows of inventory.

inventory.head(10)


# In[59]:


# 3. The first 10 rows represent data from your Staten Island location. Select these rows and save them to staten_island.

staten_island = inventory.iloc[:10,:]
staten_island


# In[60]:


# 4. A customer just emailed you asking what products are sold at your Staten Island location. 
#Select the column product_description from staten_island and save it to the variable product_request.

product_request = staten_island["product_description"]
product_request


# In[61]:


#5. Another customer emails to ask what types of seeds are sold at the Brooklyn location.

#Select all rows where location is equal to Brooklyn and product_type is equal to seeds and save them to the variable seed_request

seed_request = inventory.loc[(inventory["location"] == "Brooklyn")& (inventory["product_type"] == "seeds")]
seed_request


# In[62]:


#6. Add a column to inventory called in_stock which is True if quantity is greater than 0 and False if quantity equals 0.

a = lambda x: "True" if x>0 else "False"
inventory["in_stock"] = inventory.quantity.apply(a) 
inventory.head(10)


# In[63]:


# 7. Petal Power wants to know how valuable their current inventory is.

# Create a column called total_value that is equal to price multiplied by quantity.

inventory["total_value"] = inventory["price"] * inventory["quantity"]
inventory.head()


# In[64]:


# 8. The Marketing department wants a complete description of each product for their catalog.

# The following lambda function combines product_type and product_description into a single string:

#combine_lambda = lambda row:
#'{} - {}'.format(row.product_type, row.product_description) Paste this function into script.py.


combine_lambda = lambda row: '{} - {}'.format(row.product_type, row.product_description)


# In[65]:


#9. Using combine_lambda, create a new column in inventory called full_description that has the complete description of each product.

inventory["full_description"] = combine_lambda(inventory)
inventory


# In[ ]:




