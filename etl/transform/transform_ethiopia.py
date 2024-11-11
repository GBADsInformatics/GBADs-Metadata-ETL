import pandas as pd
import sys
import os

def replace_values(series, to_replace, value):
	for i in to_replace:
		series = series.str.replace(i, value, regex=False)
	return series

def prep_for_df(final_cats, cat, out_path, dict):

	years = []

	num_cats = len(final_cats)
	for i in range(2003, 2021):
		year = [i] * num_cats
		years.append(year)
	final_cats = [final_cats] * 18
	final_cats = [item for sublist in final_cats for item in sublist]
	years_list = [item for sublist in years for item in sublist]
	table_name = cat_table_dict.get(cat)
	table_name = [table_name] * len(final_cats)
	d = {'species': final_cats, 'year': years_list, 'table_name': table_name}
	df = pd.DataFrame(d)
	out_file(out_path, df, cat)

def prep_cats(df):
	cats = df.iloc[:,0].dropna()
	cats = replace_values(cats, to_replace, '').to_list()
	cats_list = []
	for cat in cats:
		cat = cat.lstrip().rstrip()
		cats_list.append(cat)
	return(cats_list)

def out_file(out_path, df, cat):
	out_name = '%s/EthCSA_%s.csv' % (out_path, cat)
	df.to_csv(out_name, index = False, sep = ';')

if __name__ == "__main__":

	cat_table_dict = {
		'Cattle': 'Number of Cattle by Age and Purpose',
		'Donkeys': 'Number of Horses, Mules, Donkeys and Camels by age and Purpose',
		'Horses': 'Number of Horses, Mules, Donkeys and Camels by age and Purpose',
		'Mules': 'Number of Horses, Mules, Donkeys and Camels by age and Purpose',
		'Camels': 'Number of Horses, Mules, Donkeys and Camels by age and Purpose',
		'Poultry': 'Poultry',
		'Sheep': 'Number of Sheep by Age and Purpose',
		'Goats': 'Number of Goats by Age and Purpose'
	}

	# Year, page, species dictionary to figure out how to clean files 
	year_page_dict = {
		2003: ['102','103','104','105'],
		2004: ['132','133','134','135'],
		2005: ['192','193','194','195'],
		2006: ['192','193','194','195'],
		2007: ['182','183','184','185'],
		2008: ['182','183','184','185'],
		2009: ['88','89','90','91'],
		2010: ['184','185','186','187'],
		2011: ['184','185','186','187'],
		2012: ['188','189','190','191'],
		2013: ['188','189','190','191'],
		2014: ['188','189', '190','191'],
		2015: ['188','189','190','191'],
		2016: ['188','189','190','191'],
		2017: ['94','95','96','97'],
		2018: ['92','93','94','95'],
		2019: ['222','223','224','225'],
		2020: ['185','186','187','188','189','190']
		}

	# Error handling to ensure that file path is provided and exists. 
	if len(sys.argv) != 3:
		sys.exit("Please provide path to file.")
	else: 
		file_path = sys.argv[1]
		out_path = sys.argv[2]
		if os.path.exists(file_path) != True:
			sys.exit("File does not exist.")

	# Get file name and year and path based on the name 
	file = os.path.basename(file_path)
	year = int(file[:-8])
	page = file [5:-4]
	page_index = year_page_dict.get(year).index(page)
	to_replace = ['a.','b.','c.','d.','e.','f.','1.','2.','3.','4.','5.','6.','7.','_','8.','total on Nov 10, 2020']

	if year == 2020:
		if page_index == 0:
			cat = 'cattle'
		elif page_index == 1:
			cat = 'sheep'
		elif page_index == 2:
			cat = 'goats'
		elif page_index == 3:
			cat = 'horses_mules'
		elif page_index == 4:
			cat = 'donkeys_camels'
		elif page_index == 5:
			cat = 'poultry'

	else:
		if page_index == 0:
			cat = 'cattle'
		elif page_index == 1:
			cat = 'sheep_goats'
		elif page_index == 2:
			cat = 'horses_mules_donkeys_camels'
		elif page_index == 3:
			cat = 'poultry'

	if cat == 'donkeys_camels' and year == 2020:
		final_cats = []
		df = pd.read_csv(file_path, skipfooter = 9, header = None, engine = 'python')
		sub_cats = ['Total','Male','Female']
		cats = prep_cats(df)
		for cat in cats: 
			for sub_cat in sub_cats:
				final_cat = '%s %s' % (sub_cat, cat)
				final_cats.append(final_cat)
		prep_for_df(final_cats, 'Donkeys', out_path, cat_table_dict)

		final_cats = []
		df = pd.read_csv(file_path, skiprows = 7, header = None)
		sub_cats = ['Male','Female']
		cats = prep_cats(df)
		for cat in cats: 
			final_cat = '%s %s' % ('Total', cat)
			final_cats.append(final_cat)
			if cat != 'Camels for milk':
				for sub_cat in sub_cats:
					final_cat = '%s %s' % (sub_cat, cat)
					final_cats.append(final_cat)
		prep_for_df(final_cats, 'Camels', out_path, cat_table_dict)

	if cat == 'horses_mules' and year == 2020: 
		final_cats = []
		sub_cats = ['Total','Male','Female']
		df = pd.read_csv(file_path, skipfooter = 7, header = None, engine = 'python')
		cats = prep_cats(df)
		for cat in cats:
			for sub_cat in sub_cats:
				final_cat = '%s %s' % (sub_cat, cat)
				final_cats.append(final_cat)
		prep_for_df(final_cats, 'Horses', out_path, cat_table_dict)

		# Mules 
		final_cats = []
		df = pd.read_csv(file_path, skiprows = 7, header = None)
		cats = prep_cats(df)
		for cat in cats:
			for sub_cat in sub_cats:
				final_cat = '%s %s' % (sub_cat, cat)
				final_cats.append(final_cat)
		prep_for_df(final_cats, 'Mules', out_path, cat_table_dict)


	if cat == 'goats' and year == 2020:
		final_cats = []
		years = []
		df = pd.read_csv(file_path)
		sub_cats = ['Male','Female']
		cats = prep_cats(df)
		for cat in cats:
			final_cat = '%s %s' % ('Total', cat)
			final_cats.append(final_cat)
			if cat != 'Dairy Goats':
				for sub_cat in sub_cats:
					final_cat = '%s %s' % (sub_cat, cat)
					final_cats.append(final_cat)
		prep_for_df(final_cats, 'Goats', out_path, cat_table_dict)

	if cat == 'sheep' and year == 2020:
		final_cats = []
		years = []
		df = pd.read_csv(file_path)
		sub_cats = ['Male','Female','Total']
		cats = prep_cats(df)
		for cat in cats:
			for sub_cat in sub_cats:
				final_cat = '%s %s' % (sub_cat, cat)
				final_cats.append(final_cat)
		prep_for_df(final_cats, 'Sheep', out_path, cat_table_dict)

	if cat == 'cattle' and year == 2020:
		final_cats = []
		years = []
		df = pd.read_csv(file_path)
		sub_cats = ['Male', 'Female']
		cats = prep_cats(df)
		for cat in cats:
			final_cat = '%s %s' % ('Total', cat)
			final_cats.append(final_cat)
			if (cat != 'Dairy cows') and (cat != 'Cows that gave milk for the last 12 months'):
				for sub_cat in sub_cats:
					final_cat = '%s %s' % (sub_cat, cat)
					final_cats.append(final_cat)

		prep_for_df(final_cats, 'Cattle', out_path, cat_table_dict)

	if cat == 'poultry' and year == 2020:
		final_cats = [] 
		years = []
		df = pd.read_csv(file_path, header = None)
		cats = df.iloc[:,0].dropna()
		cats = replace_values(cats, to_replace, '').to_list()
		sub_cats = ['Total','Indigenous','Hybrid','Exotic']
		for cat in cats:
			for sub_cat in sub_cats:
				final_cat = '%s %s' % (sub_cat, cat.lstrip().rstrip())
				final_cats.append(final_cat)

		num_cats = len(final_cats)
		for i in range(2003, 2021):
			year = [i] * num_cats
			years.append(year)

		# Prep for dataframe
		prep_for_df(final_cats, 'Poultry', out_path, cat_table_dict)
