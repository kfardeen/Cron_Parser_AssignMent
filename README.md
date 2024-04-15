# Cron examplepression Parser Assignment

Python Project for parsing Cron examplepression using CLI. 

Supported features:
- TEXT format for months (example: `JAN-MAR`)
- TEXT format for weekdays (example: `MON-WED`)
- comma separated values (example: `1,2,3,4,5,6,7,8`)
- intervals using slashes (example: `*/10`)
- asterisk keyword (`*`)
- ranges using hyphens (example: `0-10`)



Note that the weekdays and monthdays numbering starts from 0 and the first weekday is Sunday.

## Installation
python with version >= 3.70. 

## Running the parser

Run the following command to parse cron examplepression:

```
python3 cron_expression_parser.py "1/20 0 1,7 * 2/6 /usr/bin/find"
```

Above command provide the following output:

```
minute        20 40
hour          0
day of month  1 7
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   6
command       /usr/bin/find
```

## Running tests
To run the tests, pytest needs to be installed.


```
poetry shell
poetry install
```

you can run your unit tests by running

```
pytest test_cron_experssion_parser.py
```
