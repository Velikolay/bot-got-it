# bot-got-it
Intent tagger prototype intended for making chat bots smart in understanding complex natural language commands.
Currently supports:
1. Basic understanding of dates like 22nd of September 2017, Jan 15th, Monday next week, last Friday, tomorrow, etc.
2. Tagging of locations in the context of travel, e.g. which is origin and which destination - Flying from Sofia[LOCATION_ORIGIN] to Barcelona[LOCATION_DESTINATION]

Combination of both for more complex travel queries: A flight to Moscow departing next thursday and coming back on jan 1st 2017

TEST
Windows only at the moment...
install python 3.x
pip install nltk

python bot-got-it.py
"crf++\crf_learn.exe" features crf_train.csv model
"crf++\crf_test.exe" -m model crf_test.csv

