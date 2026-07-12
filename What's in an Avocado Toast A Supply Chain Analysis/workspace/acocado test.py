# %% [markdown]
# # What's in an Avocado Toast: A Supply Chain Analysis
# 
# ![](avocado_wallpaper.jpeg)
# 
# You find yourself in London, crafting a delectable avocado toast, a dish that has risen dramatically in popularity on breakfast menus since the 2010s. This straightforward recipe requires just five ingredients: a ripe avocado, half a lemon, a generous pinch of salt flakes, two slices of sourdough bread, and a good drizzle of extra virgin olive oil. Most of these ingredients are now staples in grocery stores, and as you will find with this project, that is no small feat!
# 
# In this project, you'll conduct a supply chain analysis of three ingredients used in avocado toast using the Open Food Facts database. This database contains extensive, openly-sourced information on various foods, including their origins. Through this analysis, you will gain an in-depth understanding of the complex supply chain involved in producing a single dish.
# 
# Three pairs of files are provided in the data folder:
# - A CSV file for each ingredient, such as `avocado.csv`, with data about each food item and countries of origin.
# - A TXT file for each ingredient, such as `relevant_avocado_categories`, containing only the category tags of interest for that food.
# 
# Here are some other key points about these files:
# - Some of the rows of data in each of the three CSV files do not contain relevant data for your investigation. In each dataset, you will need to filter out rows with irrelevant data, based on values in the `categories_tags` column. Examples of categories are fruits, vegetables, and fruit-based oils. Filter the DataFrame to include only rows where `categories_tags` contains one of the tags in the relevant categories for that ingredient.
# - Each row of data usually has multiple category tags in the `categories_tags` column.
# There is a column in each CSV file called `origins_tags`, which contains strings for the country of origin of each item.
# 
# After completing this project, you'll be armed with a list of ingredients and their countries of origin and be well-positioned to launch into other analyses that explore how long, on average, these ingredients spend at sea.
# 
# [Open Food Facts database](https://world.openfoodfacts.org/)

# %%
### Read in the avocado data

# Read tab-delimited data
import pandas as pd
avocado = pd.read_csv('data/avocado.csv', sep='\t')

# Subset large DataFrame to include only relevant columns
subset_columns = [ 'code', 'lc', 'product_name_en', 'quantity', 'serving_size', 'packaging_tags', 'brands', 'brands_tags', 'categories_tags', 'labels_tags', 'countries', 'countries_tags', 'origins','origins_tags']
avocado = avocado[subset_columns]

# Gather relevant categories data for avocados
with open("data/relevant_avocado_categories.txt", "r") as file:
    relevant_avocado_categories = file.read().splitlines()
    file.close()
    
### Filter avocado data using relevant category tags

# Turn a column of comma-separated tags into a column of lists
avocado['categories_list'] = avocado['categories_tags'].str.split(',')

# Drop rows with null values in a particular column
avocado = avocado.dropna(subset = 'categories_list')

# Filter a DataFrame based on a column of lists
avocado = avocado[avocado['categories_list'].apply(lambda x: any([i for i in x if i in relevant_avocado_categories]))]

### Where do most avocados come from?

# Filter DataFrame for UK data
avocados_uk = avocado[(avocado['countries']=='United Kingdom')]

# Find most common country for avocado origin
avocado_origin = (avocados_uk['origins_tags'].value_counts().index[0])
avocado_origin = avocado_origin.lstrip("en:")


### Create a general function to read and filter data for a particular ingredient, 
###    and return the top origin country for that food item

def read_and_filter_data(filename, relevant_categories):
  df = pd.read_csv('data/' + filename, sep='\t')
  
  # Subset large DataFrame to include only relevant columns
  subset_columns = [ 'code', 'lc', 'product_name_en', 'quantity', 'serving_size', 'packaging_tags', 'brands', 'brands_tags', 'categories_tags', 'labels_tags', 'countries', 'countries_tags', 'origins','origins_tags']
  df = df[subset_columns]

  # Split tags into lists
  df['categories_list'] = df['categories_tags'].str.split(',')

  # Drop rows with null categories data
  df = df.dropna(subset = 'categories_list')

  # Filter data for relevant categories
  df = df[df['categories_list'].apply(lambda x: any([i for i in x if i in relevant_categories]))]
    
  # Filter data for the UK
  df_uk = df[(df['countries']=='United Kingdom')]

  # Find top origin country string with the highest count
  top_origin_string = (df_uk['origins_tags'].value_counts().index[0])

  # Clean up top origin country string
  top_origin_country = top_origin_string.lstrip("en:")
  top_origin_country = top_origin_country.replace('-', ' ')

  print(f'**{filename[:-4]} origins**','\n', top_origin_country, '\n')

  print ("Top origin country: ", top_origin_country)
  print ("\n")

  # End of function - return top origin country for this ingredient
  return top_origin_country


# Analyze avocado origins again, this time by calling function
top_avocado_origin = read_and_filter_data('avocado.csv',relevant_avocado_categories)

### Repeat process above with new function for the other 2 ingredients

# Gather relevant categories data for olive oil
with open("data/relevant_olive_oil_categories.txt", "r") as file:
    relevant_olive_oil_categories = file.read().splitlines()
    file.close()

# Call user-defined function on olive_oil.csv
top_olive_oil_origin = read_and_filter_data('olive_oil.csv',relevant_olive_oil_categories)

# Gather relevant categories data for sourdough
with open("data/relevant_sourdough_categories.txt", "r") as file:
    relevant_sourdough_categories = file.read().splitlines()
    file.close()

# Call user-defined function on sourdough.csv
top_sourdough_origin = read_and_filter_data('sourdough.csv',relevant_sourdough_categories)



