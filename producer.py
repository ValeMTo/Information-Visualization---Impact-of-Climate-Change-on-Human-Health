from tools import *

if __name__ == '__main__':

    NET_EMISSION_FILE_PATH = './/sdg_13_10_esmsip2.sdmx//UNFCCC_v26.csv'
    MED_FILE_PATH = "./HFA_212_RESPIRATORY_EN.xlsx"
    POPULATION_FILE_PATH = "./tps00001.tsv/tps00001.tsv"

    PER_INHABITANTS = 100000
    scale = 0.15
    YEAR = 2015
    DISEASE = "RESPIRATORY"
    
    grouped_df, europe, pop_df = get_world(POPULATION_FILE_PATH, NET_EMISSION_FILE_PATH)
    med_selected_countries = get_med_data(europe, MED_FILE_PATH)

    selected_countries, min_value, max_value = compute_heatmap_per_year(YEAR, europe, grouped_df)
    points_df, med_selected_countries = compute_points(pop_df, med_selected_countries, YEAR, PER_INHABITANTS, scale)
    plot_heatmap(selected_countries, med_selected_countries, europe, min_value, max_value, points_df, DISEASE, YEAR)
