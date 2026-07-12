# %% [markdown]
# ![gym](gym.png)
# 

# %% [markdown]
# You are a product manager for a fitness studio and are interested in understanding the current demand for digital fitness classes. You plan to conduct a market analysis in Python to gauge demand and identify potential areas for growth of digital products and services.
# 
# ### The Data
# 
# You are provided with a number of CSV files in the "Files/data" folder, which offer international and national-level data on Google Trends keyword searches related to fitness and related products. 
# 
# ### workout.csv
# 
# | Column     | Description              |
# |------------|--------------------------|
# | `'month'` | Month when the data was measured. |
# | `'workout_worldwide'` | Index representing the popularity of the keyword 'workout', on a scale of 0 to 100. |
# 
# ### three_keywords.csv
# 
# | Column     | Description              |
# |------------|--------------------------|
# | `'month'` | Month when the data was measured. |
# | `'home_workout_worldwide'` | Index representing the popularity of the keyword 'home workout', on a scale of 0 to 100. |
# | `'gym_workout_worldwide'` | Index representing the popularity of the keyword 'gym workout', on a scale of 0 to 100. |
# | `'home_gym_worldwide'` | Index representing the popularity of the keyword 'home gym', on a scale of 0 to 100. |
# 
# ### workout_geo.csv
# 
# | Column     | Description              |
# |------------|--------------------------|
# | `'country'` | Country where the data was measured. |
# | `'workout_2018_2023'` | Index representing the popularity of the keyword 'workout' during the 5 year period. |
# 
# ### three_keywords_geo.csv
# 
# | Column     | Description              |
# |------------|--------------------------|
# | `'country'` | Country where the data was measured. |
# | `'home_workout_2018_2023'` | Index representing the popularity of the keyword 'home workout' during the 5 year period. |
# | `'gym_workout_2018_2023'` | Index representing the popularity of the keyword 'gym workout' during the 5 year period.  |
# | `'home_gym_2018_2023'` | Index representing the popularity of the keyword 'home gym' during the 5 year period. |

# %%
# Import the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# %%
df = pd.read_csv("data/workout.csv")

# convert month to datetime (safe step)
df["month"] = pd.to_datetime(df["month"])

# find row with max interest
peak_row = df.loc[df["workout_worldwide"].idxmax()]

# extract year as string
year_str = str(peak_row["month"].year)

print(year_str)

df2 = pd.read_csv("data/three_keywords.csv")
df2["month"] = pd.to_datetime(df2["month"])

# make sure values are numeric
cols = ["home_workout_worldwide", "gym_workout_worldwide", "home_gym_worldwide"]
df2[cols] = df2[cols].apply(pd.to_numeric, errors="coerce")

# -----------------------------
# COVID period (2020–2021)
# -----------------------------
covid_df = df2[(df2["month"].dt.year >= 2020) & (df2["month"].dt.year <= 2021)]

covid_means = covid_df[cols].mean()

peak_covid = covid_means.idxmax().replace("_worldwide", "")

# -----------------------------
# Current (latest month)
# -----------------------------
latest_row = df2.loc[df2["month"].idxmax()]

current = latest_row[cols].astype(float).idxmax().replace("_worldwide", "")

df3 = pd.read_csv("data/workout_geo.csv")

filtered = df3[df3["country"].isin(["United States", "Australia", "Japan"])]
top_country = filtered.loc[filtered["workout_2018_2023"].idxmax(),"country"]


df4 = pd.read_csv("data/three_keywords_geo.csv")

# remove possible hidden spaces in column names
df4.columns = df4.columns.str.strip()

# filter countries
fil = df4[df4["Country"].isin(["Philippines", "Malaysia"])]

# find which has higher home workout interest
home_workout_geo = fil.loc[
    fil["home_workout_2018_2023"].idxmax(),
    "Country"
]



# %%



