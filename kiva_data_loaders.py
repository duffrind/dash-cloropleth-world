'''
Author: Richard Decal

Helper funcs for loading kiva csvs from the relative data/ dir
'''

import pandas as pd


def load_all():
    loans_data = load_loan_data()
    mpi_location_data = load_locations_data()
    loan_theme_ids_data = load_theme_id_data()
    loan_themes_by_region_data = load_loan_themes_by_region_data()
    return loans_data, mpi_location_data, loan_theme_ids_data, loan_themes_by_region_data


def load_loan_data():
    return pd.read_csv("data/kiva_loans.csv")


def load_locations_data():
    return pd.read_csv("data/kiva_mpi_region_locations.csv")


def load_theme_id_data():
    return pd.read_csv("data/loan_theme_ids.csv")


def load_loan_themes_by_region_data():
    return pd.read_csv("data/loan_themes_by_region.csv")


