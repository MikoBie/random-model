## Load libraries
library(tidyverse)

## Randomization in the compare_df part followed the equation:
## idx - ids %% 2
## Based on it, I decided whether series_1 should be displayed
## on the left side or right. If the equation took the value
## of 1 series_0 was displayed on the left side.

## The visible and invisible condition was assigned based
## on the id. People with even id were in invisible 
## condition while people with odd in visible conditions.
## Be careful case R does not want to compute modulo
## division with big numbers.

## People who took part in the study earlier first 
## generated numbers and later solve the comparison
## task. People who completed the study in September
## had the procedure the other way around.


## Define global variables
ROOT <- here::here()
DATA <- file.path(ROOT, "data")
RAW <- file.path(DATA, 'raw')
STUDY1 <- file.path(RAW, 'study1')

## List the names of all files
list_files <- list.files(STUDY1, pattern = '*.csv')

## Create empty data frames
random_df <- tibble()
compare_df <- tibble()

## Iterate over all result files
for (file_name in list_files){
  ## Extract information whether participants first solved the generation
  ## task or comparison. 
  condition <- str_extract(file_name, pattern = '(?<=\\d{4}-\\d)\\d') %>%
    as.numeric() %>%
    { . %/% 9 }
  
  ## Create a temporary file with the random genration results of an individual participant
  temp_file <- read.csv(file.path(STUDY1,file_name)) %>%
    select(key = key_resp_5.keys, rt = key_resp_5.rt, id = id, sex = 'Płeć.', age = 'Wiek.') %>%
    filter(key != '') %>%
    mutate(condition = condition,
           key = map_chr(key, str_extract, 'period|comma'),
           rt = map_chr(rt, str_extract, '\\d\\.\\d*') %>% as.numeric(),
           ids = 1:n(),
           condition_vis = str_remove_all(id, pattern = '[a-z]') %>%
             str_extract(pattern = '\\d$') %>%
             as.numeric() %>%
             {. %% 2},
           condition_vis = if_else(condition_vis == 1, 'visible', 'invisible'),
           file_name = file_name)  %>%
    filter(key != 0) %>%
    mutate(key = if_else(key == 'comma', 0, 1),
           sex = if_else(sex == 'Kobieta', 'female', 'male'))
  
  ## Create the data set with the results of the random generation task for all participants
  random_df <- rbind(random_df, temp_file) 
  
  ## Create a temporary file with the randomness judgment results of an individual participant
  temp_file2 <- read.csv(file.path(STUDY1,file_name)) %>%
    select(key = key_resp_7.keys, rt = key_resp_7.rt, id = id, sex = 'Płeć.', age = 'Wiek.', ids = trials_2.thisIndex, idx = trials_2.thisN, comparison) %>%
    filter(key != '') %>%
    mutate(condition = condition,
           left = if_else((idx - ids)%%2 == 1, 'series_1', 'series_0'),
           correctness = case_when((key == 'f') & (comparison == left) ~ 1, 
                                   (key == 'j') & (comparison != left) ~ 1,
                                   TRUE ~ 0),
           condition_vis = str_remove_all(id, pattern = '[a-z]') %>%
             str_extract(pattern = '\\d$') %>%
             as.numeric() %>%
             {. %% 2},
           condition_vis = if_else(condition_vis == 1, 'visible', 'invisible'),
           file_name = file_name)  %>%
    filter(key != 0) %>%
    mutate(sex = if_else(sex == 'Kobieta', 'female', 'male'))
  
  ## Create the data set with the results of the randomness judgment task for all participants
  compare_df <- rbind(compare_df,temp_file2)
}

## Remove files with less than 10 rows
delete_rows <- random_df %>%
  group_by(id, file_name) %>%
  summarise(count = n()) %>% 
  filter(count < 10) %>%
  pull(file_name)

## Create a random generation data set and write it out to a file
random_df %>%
  filter(!(file_name %in% delete_rows)) %>%
  write.csv(file.path(DATA, 'study1_random_df.csv'), row.names = FALSE)

## Create a randomness judgment data set and write it out to a file
compare_df %>%
  write.csv(file.path(DATA, 'compare_df.csv'), row.names = FALSE)



