#!/usr/bin/Rscript --vanilla

library(csodata)
library(tidyverse)
library(dplyr)

# This function was adapted from the R package csodata to dump json-stat response without altering it
cso_download_tbl <- function(table_code) {
  table_code <- toupper(table_code)
  url <- paste0("https://ws.cso.ie/public/api.jsonrpc?data=%7B%22jsonrpc%22:%222.0%22,%22method%22:%22PxStat.Data.Cube_API.ReadDataset%22,%22params%22:%7B%22class%22:%22query%22,%22id%22:%5B%5D,%22dimension%22:%7B%7D,%22extension%22:%7B%22pivot%22:null,%22codes%22:false,%22language%22:%7B%22code%22:%22en%22%7D,%22format%22:%7B%22type%22:%22JSON-stat%22,%22version%22:%222.0%22%7D,%22matrix%22:%22",
                table_code,"%22%7D,%22version%22:%222.0%22%7D%7D"
  )
  
  error_message =  paste0("Failed retrieving table. Please check internet ",
                          "connection and that data .cso.ie is online")
  
  response <- tryCatch({
    httr::GET(url)
  }, warning = function(w) {
    print(paste0("Warning: ", error_message))
    return(NULL)
  }, error = function(e) {
    message(paste0("Connection Error: ", error_message))
    return(NULL)
  })
  
  #Cut off if theres issues                   
  if(is.null(response)){return(NULL)}
  
  # Check if data valid 
  if (httr::status_code(response) == 200 &&
      !all(response[["content"]][1:32] ==
           charToRaw("invalid Maintable format entered"))) {
    json_data <- rawToChar(response[["content"]])
    temp_json <- jsonlite::fromJSON(json_data)
    json_data <- jsonlite::toJSON(temp_json$result, auto_unbox = TRUE )
    return(json_data)
  } else {
    stop("Not a valid table code. See cso_get_toc() for all valid tables.")
  }
}
# Search for datasets --------------------------

## Get all datasets related to the list of 
search_terms <- c('livestock','cattle','bovine','pig','swine','chicken','poultry','goat','sheep','cow','buffalo','farm')


datalist = list()

for (i in search_terms) {

  output <- cso_search_toc(i)
  output <- data.frame(output)
  datalist[[i]] <- output
}

out_df <- do.call(rbind, datalist)

# Filter datasets --------------------------

# Based on the results from the search, the following codes refer to datasets with information about livestock data
codes <- c('AAA07','AAA03','ACEN1','AVA11','AVA12','FSA14','AAA09','AAA01','AAA08','AAA11','AAA10','AAA04','AAA05','AAA02','AAA06')

popn_df <- filter(out_df, id %in% codes)

# Convert to tibble for easy wrangling 
popn_df <- as_tibble(popn_df)

write.csv(popn_df, '../../data/raw/ireland/datasets.csv')

# Get data and metadata --------------------------

for (i in codes){
  
  df_name <- paste0(i)
  
  meta_name <- paste('../../data/raw/ireland/meta', i, sep='_')
  
  assign(df_name, cso_get_data(i))
  
  metadata <- jsonlite::fromJSON((cso_download_tbl(i)))
  
  metadata_json <- jsonlite::toJSON(metadata)
  
  assign(meta_name, metadata_json)
  
  # Write metadata 
  write(metadata_json, file = paste(meta_name, 'json', sep='.'))
  
}