## Load libraries
library(tidyverse)
library(jsonlite)

## Define global variables
ROOT <- here::here()
DATA <- file.path(ROOT, 'data')
RAW <- file.path(DATA, 'raw')
STUDY2 <- file.path(RAW, 'study2')

## Create empty data frames
list_files <- list.files(STUDY2, pattern = '*.csv')
random_df <- tibble()
digit_answer <- tibble()
simple_recall <- tibble()
complex_recall <- tibble()

## Load file files names grouped by the order condition. 
conditions <- stream_in((file(file.path(RAW, 'conditions.json')))) %>%
  unnest_longer(condition_generation_first) %>%
  unnest_longer(condition_generation_second) %>%
  pivot_longer(names_to = 'condition',
               values_to = 'id',
               cols = condition_generation_first:condition_generation_second) %>%
  distinct(id, .keep_all = TRUE) %>%
  mutate(id = str_extract(id, '.+?(?=_)'))

## Iterate over all results files
for (file_name in list_files){
  ## Create a temporary file with the random generation task results for an individual participant
	temp_file <- read.csv(file.path(STUDY2, file_name)) %>%
		select(key = key_resp_13.keys, rt = key_resp_13.rt, id = participant, sex = 'Płeć', age = 'Wiek.') %>%
		filter(key != '') %>%
		mutate(key = str_extract(key, 'period|comma'),
		       rt = str_extract(rt, '\\d\\.\\d*')) %>%
		mutate(ids = 1:n(),
		       rt = as.numeric(rt)) %>%
		filter(key != 0) %>%
		mutate(key = if_else(key == 'comma', 0, 1),
			   sex = if_else(sex == 'Kobieta', 'female', 'male'))
	
	## Create the data set with the results of the random generation task for all participants
	random_df <- rbind(random_df, temp_file)

	## Create a temporary file with the working memory capacity test results for an individual participant
	temp_file2 <- read.csv(file.path(STUDY2, file_name), na.strings = c('', NA)) %>%
		select(id = participant, simple_recall, simple_recall_rt = key_resp_5.rt,
		       simple_recall_corr, simple_recall_corrkeys, digit_answer, 
			   digit_answer_corr = key_resp.corr, digit_answer_rt = key_resp.rt,
			   operation_answer = Operation_answer, task = Task,
			   practice_complex_digit_answer = key_resp_11.keys, 
			   practice_complex_digit_answer_rt = key_resp_11.rt,
			   operation_correct, complex_recall_practice,
			   complex_recall_practice_rt = key_resp_9.rt,
			   complex_recall_pracitce_corr = complex_prac_corr,
			   trial_digit_answer = key_resp_7.keys,
			   trial_digit_answer_rt = key_resp_7.rt,
			   trial_digit_answer_corr = key_resp_7.corr, 
			   complex_recall, complex_recall_rt = key_resp_8.rt,
			   complex_recall_corr, complex_recall_corrkeys)
	
	## Process the temporary file
  temp_file2 <- temp_file2[rowSums(is.na(temp_file2)) != 22,] %>%
	  mutate(simple_recall_corrkeys = str_remove_all(simple_recall_corrkeys, '\n'),
	         simple_recall = toupper(simple_recall),
	         complex_recall_corrkeys = str_remove_all(complex_recall_corrkeys, '\n'),
	         complex_recall = toupper(complex_recall),
	         simple_recall_corr_bis = if_else(simple_recall == simple_recall_corrkeys, 1, 0),
	         complex_recall_corr_bis = if_else(complex_recall == complex_recall_corrkeys, 1, 0))

  ## Create a temporary file with the simple recall results
  simple_recall_temp <- temp_file2 %>%
    select(id, simple_recall, simple_recall_corr, simple_recall_corrkeys,
           simple_recall_rt, simple_recall_corr_bis) %>%
    filter(!is.na(simple_recall))
  ## Create a temporary file with the coplex recall results
  complex_recall_temp <- temp_file2 %>%
    select(id, complex_recall, complex_recall_corr, complex_recall_corrkeys,
           complex_recall_rt, complex_recall_corr_bis) %>%
    filter(!is.na(complex_recall))
  
  ## Create a temproary file with the operation results
  digit_answer_temp <- temp_file2 %>%
    select(id, trial_digit_answer, trial_digit_answer_corr, trial_digit_answer_rt,
           operation_answer) %>%
    filter(!is.na(trial_digit_answer))
  
  ## Create the data set with the results of the operation task for all participants
  digit_answer <- rbind(digit_answer, digit_answer_temp)
  
  ## Create the data set with the results of the simple recall for all participants
  simple_recall <- rbind(simple_recall, simple_recall_temp)
  
  ## Create the data set with the results of the complex recall for all participants
  complex_recall <- rbind(complex_recall, complex_recall_temp)
}

## Compute the ratio of good answers in the operation task
digit_answer <- digit_answer %>% 
  group_by(id) %>% 
  summarise(correct_digits = sum(trial_digit_answer_corr)/n())

## Compute the partial and absolute results of the simple recall
simple_recall <- simple_recall %>% 
  mutate(capacity_simple = nchar(simple_recall_corrkeys)) %>%
  group_by(id, capacity_simple) %>%
  summarise(correct_simple = sum(simple_recall_corr),
            n = n(),
            capacity_simple = max(capacity_simple),
            absolute_correct_simple = floor(correct_simple/n)) %>%
  group_by(id) %>%
  summarise(absolute_correct_simple = sum(absolute_correct_simple),
            partial_correct_simple = sum(correct_simple),
            capacity_simple = max(capacity_simple))

## Compute the partial and absolute results of the complex recall
complex_recall <- complex_recall %>% 
  mutate(capacity_complex = nchar(complex_recall_corrkeys)) %>%
  group_by(id, capacity_complex) %>%
  summarise(correct_complex = sum(complex_recall_corr),
            n = n(),
            capacity_complex = max(capacity_complex),
            absolute_correct_complex = floor(correct_complex/n)) %>%
  group_by(id) %>%
  summarise(absolute_correct_complex = sum(absolute_correct_complex),
            partial_correct_complex = sum(correct_complex),
            capacity_complex = max(capacity_complex))

## Create a working memory data set and write it out to a file
digit_answer %>%
  left_join(simple_recall) %>%
  left_join(complex_recall) %>%
  write.csv(file.path(DATA, 'wm_df.csv'), row.names = FALSE)

## Create a random generation data set and write it out to a file
random_df %>% 
  inner_join(conditions) %>%
  write.csv(file.path(DATA, 'study2_random_df.csv'), row.names = FALSE)

