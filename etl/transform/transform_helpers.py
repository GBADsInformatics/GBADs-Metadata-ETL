import json
import pandas as pd

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

def get_cat_yr(df, cat_col, year_col):
    """
    Extracts unique categories and the years that they occur in from the 'Item' column of the input DataFrame.

    Parameters:
    df (pd DataFrame): Input DataFrame containing columns named 'Item' and 'Year'.

    Returns:
    pd DataFrame: DataFrame containing unique categories extracted from the 'Item' column and the years that they occur in.
    """
    
    df_cat_yrs = df.groupby([cat_col])[year_col].unique().apply(list).reset_index()

    df_cat_yrs.columns = ['category','year']
    
    return(df_cat_yrs)

def get_cols(df):
    """
    Get columns from the dataset
    """

    return(list(df.columns))

def get_cat(df, col_name, out_col_name):
    """
    Extracts unique categories from the 'Item' column of the input DataFrame.

    Parameters:
    df (pd DataFrame): Input DataFrame containing a column named 'Item'.

    Returns:
    pd DataFrame: DataFrame containing unique categories extracted from the 'Item' column.
    """

    cats = df[col_name].unique()

    df_cats = pd.DataFrame(cats, columns = [out_col_name])

    return(df_cats)

def load_from_json(json_file_path):

    with open(json_file_path, 'r') as file:
        dataset = json.load(file)

    return dataset