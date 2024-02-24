import pandas as pd 
from extract_helpers import GBADsAPI as gapi

def createEthDescriptions(output_path):

    """
    Creates descriptions for Ethiopia CSA tables based on table names in the GBADs API

    Parameters: 
    - output_path (str): Path to save csv file 
    """

    eth_tbls = gapi.get_eth_tbls()
    tbls = pd.DataFrame({'tbl_name':eth_tbls})

    tbls['description'] = ''

    nRows = tbls.shape[0]

    for i in range(0, nRows):
        tbl = tbls['tbl_name'].iloc[i]
        species = tbl.split('_')[2]
        if 'population' in tbl: 
            if species == 'camels' or species == 'donkeys' or species == 'horses' or species == 'mules':
                description = 'Number of %s by sex and age' % species
            else:
                description = 'Number of %s by sex, age, and breed (exotic, indigenous, hybrid)' % species
        elif 'dairy' in tbl:
            description = 'Number of dairy %s, milk production, and lactation period' % species
        elif 'estimation' in tbl:
            description = 'Estimated number of %s birthed, purchased, acquired, sold, slaughtered or offered' % species
        elif 'health' in tbl:
            description = 'Estimated number of %s vaccinated, afflicted/diseased, treated, or died' % species 
        elif 'holdings' in tbl: 
            description = 'Number of %s holdings' % species 
        elif 'usage' in tbl: 
            description = 'Number of %s by usage' % species 
        elif 'eggs' in tbl:
            description = 'Total egg production by breed and total number of laying birds'
        elif 'inventory' in tbl: 
            description = 'Poultry inventory by type'
        else: 
            print('%s does not have a description' % tbl)
        tbls['description'].iloc[i] = description

    tbls.to_csv('output_path/eth_regions_tbls_description.csv', index=False)