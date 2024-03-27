import json
import pandas as pd
from datetime import datetime 

def write_metadata(out_path, data, source_table):

    date = datetime.today().strftime('%Y%m%d')

    outname = '%s/%s_%s_Dataset.csv' % (out_path, date, source_table)

    with open(outname, 'w') as json_file:
        json.dump(data, json_file) 

def write_parent_child(out_path, df, source_table, keyword):

    date = datetime.today().strftime('%Y%m%d')

    outname = '%s/%s_%s_%s.csv' % (out_path, date, source_table, keyword)

    df.to_csv(outname, index=False)

def get_descriptions_txt(file_path):

    with open(file_path, 'r') as file:
        data = file.read().replace('\n', '')
    
    return(data)

def get_temporal_coverage(df, date_col):

    temporalCoverage = '%s/%s' % (df[date_col].min(), df[date_col].max())

    return(temporalCoverage)

def get_cat_yr_area(df, cat_col, area_col, year_col):
    """
    Extracts unique categories and the years and countries that they occur in from the 'Item' column of the input DataFrame.

    Parameters:
    df (pd DataFrame): Input DataFrame containing columns named 'Item', 'Year', and 'Area'.

    Returns:
    pd DataFrame: DataFrame containing unique categories extracted from the 'Item' column and the years and countries that they occur in.
    """

    df_cat_yr_area = df.groupby([cat_col, area_col])[year_col].unique().apply(list).reset_index()
    
    df_cat_yr_area.columns = ['category','area','year']

    return(df_cat_yr_area)

def get_cat_yr(df, cat_col, year_col, columns = ['category','year']):
    """
    Extracts unique categories and the years that they occur in from the 'Item' column of the input DataFrame.

    Parameters:
    df (pd DataFrame): Input DataFrame containing columns named 'Item' and 'Year'.

    Returns:
    pd DataFrame: DataFrame containing unique categories extracted from the 'Item' column and the years that they occur in.
    """
    
    df_cat_yrs = df.groupby([cat_col])[year_col].unique().apply(list).reset_index()

    df_cat_yrs.columns = columns
    
    return(df_cat_yrs)

def get_cols(df):
    """
    Get columns from the dataset
    """

    return(list(df.columns))

def get_cat(df, col_name):
    """
    Extracts unique categories from the 'Item' column of the input DataFrame.

    Parameters:
    df (pd DataFrame): Input DataFrame containing a column named 'Item'.

    Returns:
    pd DataFrame: DataFrame containing unique categories extracted from the 'Item' column.
    """

    cats = df[col_name].unique().tolist()

    return(cats)

def load_from_json(json_file_path):

    with open(json_file_path, 'r') as file:
        dataset = json.load(file)

    return dataset