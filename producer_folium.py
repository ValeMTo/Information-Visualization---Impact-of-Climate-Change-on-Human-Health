from tools import *
import folium

if __name__ == '__main__':

    NET_EMISSION_FILE_PATH = './/sdg_13_10_esmsip2.sdmx//UNFCCC_v26.csv'
    MED_FILE_PATH = "./HFA_212_RESPIRATORY_EN.xlsx"
    POPULATION_FILE_PATH = "./tps00001.tsv/tps00001.tsv"
    FILE_TO_SAVE = '2018_Respiratory.html'

    PER_INHABITANTS = 100000
    scale = 0.15
    YEAR = 2018
    DISEASE = "RESPIRATORY"
    
    grouped_df, europe, pop_df = get_world(POPULATION_FILE_PATH, NET_EMISSION_FILE_PATH)
    med_selected_countries = get_med_data(europe, MED_FILE_PATH)

    selected_countries, min_value, max_value = compute_heatmap_per_year(YEAR, europe, grouped_df)
    points_df, med_selected_countries = compute_points(pop_df, med_selected_countries, YEAR, PER_INHABITANTS, scale)
    plot_heatmap(selected_countries, med_selected_countries, europe, min_value, max_value, points_df, DISEASE, YEAR)

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world['centroid'] = world.geometry.centroid
    centroid_gdf = world[['name', 'geometry']]

    year_data = grouped_df[grouped_df['Year'] == YEAR]
    year_data = year_data.drop(columns=['Year'])
    year_data = year_data.merge(centroid_gdf, left_on='name', right_on='name')

    gdf = gpd.GeoDataFrame(year_data, geometry='geometry')
    gdf.crs = "EPSG:4326"
    geojson_path = 'countries_emissions.geojson'
    gdf.to_file(geojson_path, driver='GeoJSON')

    m = folium.Map(location=[47.5162, 14.5501], zoom_start=4)  # Austria's approximate center

    choropleth = folium.Choropleth(
        geo_data=geojson_path,
        name='Emissions',
        data=year_data,
        columns=['name', 'emissions'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Emissions Intensity',
        highlight=True,
        nan_fill_color='black'  # or 'white' as per your comment
    ).add_to(m)

    points_gdf = gpd.GeoDataFrame(points_df, geometry='geometry')
    points_gdf.crs = gdf.crs
    marker_group = folium.FeatureGroup(name='Respiratory Deaths scale: ' + str(scale))

    for idx, row in points_gdf.iterrows():
        folium.CircleMarker(
            location=[row['geometry'].y, row['geometry'].x],
            radius=0.01,  # Small radius for small points
            color='black',  # Orange color for the point
            fill=False,
            fill_opacity=0.0001,
            legend_name='Respiratory Deaths',
            popup=row['name']  # Popup text, can be changed to something else
        ).add_to(marker_group)

    marker_group.add_to(m)

    folium.LayerControl().add_to(m)
    m.save(FILE_TO_SAVE)
