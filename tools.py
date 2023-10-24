import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import tqdm

import os

import geopandas as gpd
import geoplotlib
from shapely.geometry import Polygon, MultiPolygon, Point

import warnings
warnings.filterwarnings('ignore')

def get_world(POPULATION_FILE_PATH, NET_EMISSION_FILE_PATH):
    pop_df = pd.read_csv(POPULATION_FILE_PATH, sep='\t', encoding='latin-1')
    pop_df['indic_de,geo\\time'] = pop_df['indic_de,geo\\time'].apply(lambda x: x.split(',')[1])
    pop_df = pop_df.applymap(lambda x: x.split(' ')[0])

    pop_df = pop_df.rename(columns={'indic_de,geo\\time': 'ISO 2'})

    values = []
    for index, row in tqdm.tqdm(pop_df.iterrows(), total=len(pop_df)):
        for col in pop_df.columns[1:]:
            value = [row['ISO 2'], col, row[col]]
            values.append(value)

    pop_df = pd.DataFrame(values, columns=['ISO 2', 'YEAR', 'Population'])
    pop_df = pop_df.replace(':', np.nan)


    # Get the world map
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    # Isolate Europe
    europe=world[world.continent=='Europe']
    #Remove Russia and Iceland
    europe=europe[(europe.name!='Russia')]
    #Clip polygon from the map of Europe
    polygon = Polygon([(-25,35), (40,35), (40,75),(-25,75)])
    europe=gpd.clip(europe, polygon) 

    enviroment_df = pd.read_csv(NET_EMISSION_FILE_PATH, encoding='ISO-8859-1')
    enviroment_df.rename(columns={'Country': 'name'}, inplace=True)
    enviroment_df['emissions'].fillna(0, inplace=True)

    grouped_df = enviroment_df.groupby(['name', 'Year' ])['emissions'].sum().reset_index()

    return grouped_df, europe, pop_df

def compute_heatmap_per_year(YEAR, europe, grouped_df):
    df = grouped_df[grouped_df['Year'] == YEAR]

    selected_countries=europe[europe.name.isin(list(df.name))]
    selected_countries=selected_countries.merge(df,on='name',how='left')
    min_value = 0
    max_value = selected_countries['emissions'].max() 
    max_value = 7201328.42322
    print(min_value, max_value)

    return selected_countries, min_value, max_value

def random_point_inside_polygon(polygon):
    # Create a bounding box around the polygon
    minx, miny, maxx, maxy = polygon.bounds
    
    while True:
        # Generate a random point within the bounding box
        random_point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        
        # Check if the random point is inside the polygon
        if polygon.contains(random_point):
            return random_point

def random_point_inside_multipolygon(multipolygon):
    # Randomly select one of the polygons in the MultiPolygon
    chosen_polygon = random.choice(list(multipolygon))
    
    return random_point_inside_polygon(chosen_polygon)

def get_med_data(europe, MED_FILE_PATH):
    med_df = pd.read_excel(MED_FILE_PATH, sheet_name='Data (table)')
    countries_df = pd.read_excel(MED_FILE_PATH, sheet_name='Countries')
    countries_df.rename(columns={'Code': 'COUNTRY_REGION'}, inplace=True)
    med_df = med_df.merge(countries_df, on='COUNTRY_REGION', how='left')
    med_df.rename(columns={'Full name': 'name'}, inplace=True)
    med_df = med_df.drop(columns=['SEX','ISO 3', 'WHO code', 'Short name'], axis=1)

    med_selected_countries=europe[europe.name.isin(list(med_df.name))]
    med_selected_countries = med_selected_countries.merge(med_df,on='name',how='left')

    return med_selected_countries

def compute_points(pop_df, med_selected_countries, YEAR, PER_INHABITANTS=100000, scale = 1):
    pop = []
    pop_df['YEAR'] = pop_df['YEAR'].astype(int)
    for index, row in tqdm.tqdm(med_selected_countries.iterrows(), total=len(med_selected_countries)):
        new_cell = pop_df[(pop_df['ISO 2'] == row['ISO 2']) & (pop_df['YEAR'] == YEAR)]['Population'].values
        if len(new_cell) == 0 or new_cell is None:
            pop.append(np.nan)
        else:
            pop.append(new_cell[0])

    med_selected_countries.reset_index(drop=True, inplace=True)
    med_selected_countries['Population'] = pop

    for index, row in tqdm.tqdm(med_selected_countries.iterrows(), total=len(med_selected_countries)):
        if row['Population'] is np.nan or row['VALUE'] is np.nan:
            med_selected_countries.at[index, 'patients'] = np.nan
        else:
            med_selected_countries.at[index, 'patients'] = (float(row['VALUE']) * int(row['Population']) / PER_INHABITANTS) * scale
    
    points = []
    med_selected_countries = med_selected_countries[med_selected_countries['YEAR'] == YEAR]
    for index, row in tqdm.tqdm(med_selected_countries.iterrows(), total=len(med_selected_countries)):
        if not pd.isna(row['patients']):
            for i in range(int(row['patients'])):
                new_row = [row['name'], random_point_inside_polygon(row['geometry'])]
                # Append the new row to the points_df DataFrame
                points.append(new_row)

    points_df = pd.DataFrame(points, columns=['name', 'geometry'])
    points_df['longitude'] = points_df['geometry'].apply(lambda p: p.x)
    points_df['latitude'] = points_df['geometry'].apply(lambda p: p.y)

    med_selected_countries = med_selected_countries.dropna(subset=['patients'])
    med_selected_countries.reset_index(drop=True, inplace=True)
    return points_df, med_selected_countries

def plot_heatmap(selected_countries, med_selected_countries, europe, min_value, max_value, points_df, disease, YEAR, dir = "./Results"):
    fig, ax = plt.subplots(1, figsize=(15, 15))
    fig.suptitle("Emissions Intensity", fontweight="bold", fontsize=15)

    not_in_data_europe = europe[~europe.name.isin(list(med_selected_countries.name.unique()))]

    europe.plot(color="whitesmoke", edgecolor="black", ax=ax)
    selected_countries.plot('emissions', cmap="Blues", edgecolor="black", ax=ax, vmin=min_value, vmax=max_value)
    not_in_data_europe.plot(color="black", edgecolor="black", ax=ax)
    points_df.plot(x="longitude", y="latitude", kind="scatter",color = 'orange',alpha=0.5, s=1, marker='.', ax=ax)

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=min_value, vmax=max_value))
    sm._A = []
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label( "Emissions VS "+ disease +" "+ str(YEAR), rotation=0, y=1.05, labelpad=-35)

    if not os.path.exists(dir):
        os.makedirs(dir)

    plt.savefig(os.path.join(dir, "Emissions VS "+ disease +" "+ str(YEAR)) +".jpeg", dpi=300)
