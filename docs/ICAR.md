# The Global Standard for Livestock Data (ICAR) Data

Data was collected from ICAR through direct download (see Section Download Information for more information about how data was downloaded)

## Extract

Data was manually extracted from the ICAR website. The data files in data/raw/icar are dated according to when the data was collected. Therefore, there are no extraction scripts associated with this data source or datasets. 

## Transform

Transform script: etl/transform/transform_icar.ipynb

Note that a notebook was used because of a change in the research protocol in my thesis. Initially, I was doing "Interoperability Assessments" for each datasource where I had a notebook for each data source, collecting data about the levels of interoperability. I have since changed the format of my thesis and wanted to reuse components of the changed experimental protocol for GBADs and for my thesis. Rather than converting the notebook into a script, I saved work and adapted the notebook to save the transformed data using the transform_helpers module that I wrote for the GBADs work. 

## Load 



## Download information

**Date of form:** 2023-11-07

**Form filled by:** Kassy Raymond

**Name of data portal:** The Global Standard for Livestock Data (ICAR)

**URL:** https://my.icar.org/stats/list

**Administrative Level (Intergovernmental, Supranational, National):** International Organization

**What is the data publication system that is used?** Unspecified. Seems to be proprietary – they listed Mtech (https://www.mtech.fi), a Finnish consulting company, on their website. They offer data integration and sharing, and master metadata management solutions. 

**How do you search for data through the interface?** Through a data viewer. You can look at the datasets available through a dropdown. There are buttons on the top to toggle species. 

<img src="../screenshots/20240122-icar.png" alt="screenshot of ICAR data download interface" style="width:600px"/>

**How many datasets report livestock agriculture population data?** 4; one for cattle, one for sheep, one for goat, and one for buffalo

## 2 Data and Metadata Information

### 2.1 Metadata 

**Is there metadata available through an API?** 
No

**Where no API is available, can you bulk download, scrape, or otherwise export the metadata?** 
I could not find metadata on the statistics portal. There is a list of recent updates, but they are not downloadable. To get these updates you would have to scrape or create a bot that checks the website on a set time interval. 

**List all formats that metadata are available in**
N/A

**Are metadata elements described using a semantic schema (DCMI, schema.org etc.)? If so, which schema is used?**
N/A

**Regardless of whether a semantic schema is used, provide a list of all metadata elements used in the metadata.**
N/A

**Is the metadata content provided using content descriptive standards (controlled vocabularies, ontologies, thesauri etc.)? If so, which content descriptive standards are used? Provide links or references when available.**
N/A

**Is licensing information provided in the metadata? If so, which license is used?** 
There was no licensing provided in the metadata or on the data portal

**Is the date of creation provided in the metadata?**
N/A 

**Is the date of last update provided in the metadata?**
There is a list of recent updates, but they are not downloadable. To get these updates you would have to scrape or create a bot that checks the website on a set time interval.

### 2.2 Data

**Where no API is available, can you bulk download, scrape, or otherwise export the data?**
Yes, you can export the data in Excel

**List all formats that data are available in:**
Excel

**Are there descriptions (structural metadata) for each of the columns?** 
No

**Is the content of the dataset (countries, dates, species etc.) described using a standard (controlled vocabulary, taxonomy, thesauri, ontology etc.) or defined?**
Not that I could find. ICAR creates standards for collecting livestock data, so it assumed that the data is collected using these standards. However, I could not find information about the content of the datasets providing summary statistics.

**Are previous versions of the data available?**
No

