__author__ = 'Nicky'
import re
import csv
from nltk.tokenize import word_tokenize

locations_en = {'sofia', 'bourgas', 'varna', 'barcelona', 'london', 'paris', 'madrid', 'berlin', 'moscow', 'tokyo', 'italy', 'spain', 'france', 'bulgaria', 'japan'}
months_en = {'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'jan', 'jan.', 'feb', 'feb.', 'mar', 'mar.', 'apr', 'apr.', 'jun', 'jul', 'jun', 'jul', 'aug', 'aug.', 'sep', 'sep.', 'oct', 'oct.', 'nov', 'nov.', 'dec', 'dec.'}
weekdays_en = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'}
#months_short_en = ['jan', 'jan.', 'feb', 'feb.', 'mar', 'mar.', 'apr', 'apr.', 'jun', 'jul', 'jun', 'jul', 'aug', 'aug.', 'sep', 'sep.', 'oct', 'oct.', 'nov', 'nov.', 'dec', 'dec.']
day_en = "^(0)?[1-9]$|^[12][0-9]$|^3[01]$|^[4-9]th$|^1[0-9]th$|^2[04-9]th$|^30th$|^1st$|^2nd$|^3rd$|^21st$|^22nd$|^23rd$|^31st$"
year = "^[0-9]{4}(y)?$"
day_en_regex = re.compile(day_en)
year_regex = re.compile(year)


day_pattern = '(0)?[1-9]|12[0-9]|3[01]'
month_pattern = '(0)?[1-9]|1[0-2]'
year_pattern = '[0-9]{4}(y)?'
date_patterns = {
    'YYYY-MM-DD': '{}-{}-{}'.format(year_pattern, month_pattern, day_pattern),
    'MM-DD-YYYY': '{}-{}-{}'.format(month_pattern, day_pattern, year_pattern),
    'MM/DD/YYYY': '{}/{}/{}'.format(month_pattern, day_pattern, year_pattern),
    'MM.DD.YYYY': '{}.{}.{}'.format(month_pattern, day_pattern, year_pattern),
    'MM/DD': '{}/{}'.format(month_pattern, day_pattern),
    'MM.DD': '{}.{}'.format(month_pattern, day_pattern),
    'MM/YYYY': '{}/{}'.format(month_pattern, year_pattern),
    'MM.YYYY': '{}.{}'.format(month_pattern, year_pattern),
    'MM-YYYY': '{}-{}'.format(month_pattern, year_pattern),
}

entities = [
    {"name": "location_en", "label": "LOCATION", "type": "set", "values": locations_en},
    {"name": "month_en", "label": "MONTH", "type": "set", "values": months_en},
    {"name": "weekday_en", "label": "WEEKDAY", "type": "set", "values": weekdays_en},
    {"name": "day_number_en", "label": "DAYNUM", "type": "regex", "values": day_en_regex},
    {"name": "year_number", "label": "YEARNUM", "type": "regex", "values": year_regex}
]

test_data = [
    "i'm coming on nov 1st 2017 and i'll bang you.",
    "14th of september 1988",
    "traveling in june with 2 kids",
    "flying out on november 7th and coming back 1st of feb 2017",
    "what are you going to do on wednesday",
    "i'm flying next thu to Moscow",
    "i'm flying this thu to Moscow",
    "i'm flying on thu to Moscow",
    "last monday i went to Moscow",
    "last tuesday",
    "this friday",
    "on sunday",
    "wednesday",
    "We decided to do cool stuff previous friday and it was a great experience",
    "next tuesday",
    "what are you going to do on wednesday this week",
    "i'm flying thu next week to Moscow",
    "i'm flying thu this week to Moscow",
    "monday last week i went to Moscow",
    "tuesday last week",
    "friday this week",
    "We decided to do cool stuff friday previous week and it was a great experience",
    "tuesday next week",
    "a flight from Japan to Bulgaria leaving mon next week and coming back on dec 24th",
    "from Moscow",
    "to Moscow",
    "from Tokyo to France",
    "flying from Madrid to Bulgaria next tuesday"
]

flight_search_train_data = [
    (
        "A flight from Sofia to Madrid on july 22, returning on 30th of jan 2017",
        "R R R LOCATION_ORIGIN R LOCATION_DESTINATION R DATESTART_MONTH DATEEND_DAYNUM R R R DATESTART_DAYNUM R DATEMEM_MONTH DATEEND_YEARNUM"
    ),
    (
        "I'm travelling from Bourgas to Barcelona monday next week",
        "R R R R LOCATION_ORIGIN R LOCATION_DESTINATION RELDATE_WEEKDAY_P1 R R"
    ),
    (
        "Going to Barcelona on friday",
        "R R LOCATION_DESTINATION R RELDATE_WEEKDAY"
    ),
    (
        "to London from Barcelona",
        "R LOCATION_DESTINATION R LOCATION_ORIGIN"
    ),
    (
        "from Italy from Spain",
        "R LOCATION_ORIGIN R LOCATION_DESTINATION"
    ),
    (
        "to Paris",
        "R LOCATION_DESTINATION"
    ),
    (
        "to Berlin",
        "R LOCATION_DESTINATION"
    ),
    (
        "from Berlin",
        "R LOCATION_ORIGIN"
    ),
    (
        "to Sofia 22nd of sep",
        "R LOCATION_DESTINATION DATESTART_DAYNUM R DATEEND_MONTH"
    ),
    (
        "departing from Sofia on february 17th",
        "R R LOCATION_ORIGIN R DATESTART_MONTH DATEEND_DAYNUM"
    )
]

dates_train_data = [
    (
        "he arrives on sep 22nd and won't stay long",
        "R R R DATESTART_MONTH DATEEND_DAYNUM R R R R R"
    ),
    (
        "I had great time on april 12th",
        "R R R R R DATESTART_MONTH DATEEND_DAYNUM"
    ),
    (
        "february 27 is my birthday",
        "DATESTART_MONTH DATEEND_DAYNUM R R R"
    ),
    (
        "the deadline is 31st of december, be ready",
        "R R R DATESTART_DAYNUM R DATEEND_MONTH R R R"
    ),
    (
        "she arrives 22 of mar.",
        "R R DATESTART_DAYNUM R DATEEND_MONTH"
    ),
    (
        "i want some place to go in october",
        "R R R R R R R DATE_MONTH"
    ),
    (
        "find me a flight in july 2017 to London",
        "R R R R R DATESTART_MONTH DATEEND_YEARNUM R R"
    ),
    (
        "people do shit in october, then they deal with it in nov.",
        "R R R R DATE_MONTH R R R R R R R DATE_MONTH R"
    ),
    (
        "i want to fly to Barcelona on 13th of april 2018 and never come back",
        "R R R R R R R DATESTART_DAYNUM R DATEMEM_MONTH DATEEND_YEARNUM R R R R"
    ),
    (
        "the building will be available on jan. 1st 2017",
        "R R R R R R DATESTART_MONTH DATEMEM_DAYNUM DATEEND_YEARNUM"
    ),
    (
        "they reported that the ceremony starts on october 11th 2020, see you there",
        "R R R R R R R DATESTART_MONTH DATEMEM_DAYNUM DATEEND_YEARNUM R R R R"
    ),
    (
        "i'm flying to Maldives is in may",
        "R R R R R R R DATE_MONTH"
    ),
    (
        "he finished 3rd on the olympic games",
        "R R R R R R R"
    ),
    (
        "he was 3rd on the olympic games in 2016",
        "R R R R R R R R DATE_YEAR"
    ),
    (
        "she became 3rd in the june competition",
        "R R R R R DATE_MONTH R"
    ),
    (
        "11th of feb 1981",
        "DATESTART_DAYNUM R DATEMEM_MONTH DATEEND_YEARNUM"
    )
]

rel_weekdays_pre_train_data = [
    (
        "flying next friday to Madrid",
        "R R RELDATE_WEEKDAY_P1 R R"
    ),
    (
        "leaving wen and returning next tuesday",
        "R RELDATE_WEEKDAY R R R RELDATE_WEEKDAY_P1"
    ),
    (
        "I will party this sat to feel like a boss",
        "R R R R RELDATE_WEEKDAY R R R R R"
    ),
    (
        "i'll be chilling on sat and you?",
        "R R R R R RELDATE_WEEKDAY R R R"
    ),
    (
        "i arrived last monday",
        "R R R RELDATE_WEEKDAY_N1"
    ),
    (
        "what did you do previous monday",
        "R R R R R RELDATE_WEEKDAY_N1"
    ),
    (
        "I went to Barcelona with my friend previous monday so we went to el classico",
        "R R R R R R R R RELDATE_WEEKDAY_N1 R R R R R R"
    ),
    (
        "last sunday was cloudy",
        "R RELDATE_WEEKDAY_N1 R R"
    ),
    (
        "sunday please",
        "RELDATE_WEEKDAY R"
    ),
    (
        "on saturday",
        "R RELDATE_WEEKDAY"
    ),
    (
        "saturday",
        "RELDATE_WEEKDAY"
    ),
    (
        "next tuesday",
        "R RELDATE_WEEKDAY_P1"
    ),
    (
        "last mon",
        "R RELDATE_WEEKDAY_N1"
    ),
    (
        "previous mon",
        "R RELDATE_WEEKDAY_N1"
    ),
    (
        "prev mon",
        "R RELDATE_WEEKDAY_N1"
    ),
    (
        "this friday",
        "R RELDATE_WEEKDAY"
    )
]

rel_weekdays_post_train_data = [
    (
        "flying friday next week to Madrid",
        "R RELDATE_WEEKDAY_P1 R R R R"
    ),
    (
        "leaving wen this week and returning next tuesday",
        "R RELDATE_WEEKDAY R R R R R RELDATE_WEEKDAY_P1"
    ),
    (
        "I will party sat this week to feel like a boss",
        "R R R RELDATE_WEEKDAY R R R R R R R"
    ),
    (
        "i'll be chilling on sat this week and you?",
        "R R R R R RELDATE_WEEKDAY R R R R R"
    ),
    (
        "i arrived monday last week",
        "R R RELDATE_WEEKDAY_N1 R R"
    ),
    (
        "what did you do monday previous week",
        "R R R R RELDATE_WEEKDAY_N1 R R"
    ),
    (
        "I went to Barcelona with my friend monday previous week so we went to el classico",
        "R R R R R R R RELDATE_WEEKDAY_N1 R R R R R R R R"
    ),
    (
        "sunday last week was cloudy",
        "RELDATE_WEEKDAY_N1 R R R R"
    ),
    (
        "sunday this week please",
        "RELDATE_WEEKDAY R R R"
    ),
    (
        "on saturday this week",
        "R RELDATE_WEEKDAY R R"
    ),
    (
        "saturday this week",
        "RELDATE_WEEKDAY R R"
    ),
    (
        "tuesday next week",
        "RELDATE_WEEKDAY_P1 R R"
    ),
    (
        "mon last week",
        "RELDATE_WEEKDAY_N1 R R"
    ),
    (
        "mon previous week",
        "RELDATE_WEEKDAY_N1 R R"
    ),
    (
        "mon prev week",
        "RELDATE_WEEKDAY_N1 R R"
    )
]


def get_word_labels(word, entities):
    labels = []
    for entity in entities:
        if entity['type'] == 'set' and word in entity['values']:
            labels.append(entity['label'])
        elif entity['type'] == 'regex' and entity['values'].match(word):
            labels.append(entity['label'])

    if labels:
        return "|".join(labels)
    else:
        return "R"


def dump_training_samples(train_data, entities):
    with open('crf_train.csv', 'w', newline='') as csvfile:
        crf_writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for tain_sample in train_data:
            words = word_tokenize(tain_sample[0])
            tags = tain_sample[1].split(" ")
            print(words)
            print(tags)
            for word, tag in zip(words, tags):
                word = word.lower()
                labels = get_word_labels(word, entities)
                crf_writer.writerow([word, labels, tag])
            crf_writer.writerow([])


def dump_test_samples(test_sent, entities):
    with open('crf_test.csv', 'w', newline='') as csvfile:
        crf_writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for sent in test_sent:
            words = word_tokenize(sent)
            print(words)
            for word in words:
                word = word.lower()
                labels = get_word_labels(word, entities)
                crf_writer.writerow([word, labels])
            crf_writer.writerow([])

if __name__ == '__main__':
    train_data = dates_train_data + rel_weekdays_pre_train_data + rel_weekdays_post_train_data + flight_search_train_data
    dump_training_samples(train_data, entities)
    dump_test_samples(test_data, entities)
