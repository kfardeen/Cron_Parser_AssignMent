from cron_base_class import (
    HourCronFieldParser,
    MinuteCronFieldParser,
    DayCronFieldParser,
    WeekDayCronFieldParser,
    MonthCronFieldParser,
    CronFieldParsingError,
)
from cron_expression_parser import CronParsingExceptionError, CronExpressionParser
import pytest


class TestValidCronExpression:
    @pytest.mark.parametrize(
        "provided_input, expected_output",
        [
            (
                    "*",
                    "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59",
            ),
            ("*/10", "0 10 20 30 40 50"),
            ("1-12", "1 2 3 4 5 6 7 8 9 10 11 12"),
        ],
    )
    def test_valid_minute_field(self, provided_input, expected_output):
        minute_field = MinuteCronFieldParser(provided_input)
        assert minute_field.evaluateExpression() == expected_output

    @pytest.mark.parametrize(
        "provided_input, expected_output",
        [
            ("*", "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23"),
            ("6-17", "6 7 8 9 10 11 12 13 14 15 16 17"),
            ("0-8", "0 1 2 3 4 5 6 7 8"),
        ],
    )
    def test_valid_hour_field(self, provided_input, expected_output):
        hour_field = HourCronFieldParser(provided_input)
        assert hour_field.evaluateExpression() == expected_output

    @pytest.mark.parametrize(
        "provided_input, expected_output",
        [
            (
                    "*",
                    "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31",
            ),
            ("10-20", "10 11 12 13 14 15 16 17 18 19 20"),
            ("1,5,10", "1 5 10"),
        ],
    )
    def test_valid_day_of_month_field(self, provided_input, expected_output):
        month_field = DayCronFieldParser(provided_input)
        assert month_field.evaluateExpression() == expected_output

    @pytest.mark.parametrize(
        "provided_input, expected_output",
        [
            ("*", "1 2 3 4 5 6 7 8 9 10 11 12"),
            ("2-7", "2 3 4 5 6 7"),
            ("1,6,7,8,9", "1 6 7 8 9"),
            ("JAN-JUN", "1 2 3 4 5 6"),
            ("JAN,FEB,MAY", "1 2 5"),
        ],
    )
    def test_valid_month_field(self, provided_input, expected_output):
        day_of_week_field = MonthCronFieldParser(provided_input)
        assert day_of_week_field.evaluateExpression() == expected_output

    @pytest.mark.parametrize(
        "provided_input, expected_output",
        [
            ("*", "0 1 2 3 4 5 6"),
            ("2-4", "2 3 4"),
            ("1,6", "1 6"),
            ("MON,WED", "1 3"),
            ("SUN-WED", "0 1 2 3"),
        ],
    )
    def test_valid_day_of_week_field(self, provided_input, expected_output):
        day_of_week_field = WeekDayCronFieldParser(provided_input)
        assert day_of_week_field.evaluateExpression() == expected_output

    @pytest.mark.parametrize(
        "provided_input, expected_output",
        [
            (
                    "*/15 8-17 * * 1-5 /usr/bin/python script.py some args",
                    [
                        "minute        0 15 30 45",
                        "hour          8 9 10 11 12 13 14 15 16 17",
                        "day of month  0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31",
                        "month         1 2 3 4 5 6 7 8 9 10 11 12",
                        "day of week   1 2 3 4 5",
                        "command       /usr/bin/python script.py some args",
                    ],
            ),
        ],
    )
    def test_cron_expression(self, provided_input, expected_output):
        parser = CronExpressionParser(provided_input)
        assert parser.describe_cron_expr().split("\n") == expected_output


class TestInValidCronExpression:
    @pytest.mark.parametrize(
        "provided_input", ["60-75", "14-3" "101", "ONE", "*/*", "12,89"]
    )
    def test_invalid_minute_field(self, provided_input):
        with pytest.raises(CronFieldParsingError):
            minute_field = MinuteCronFieldParser(provided_input)
            minute_field.evaluateExpression()

    @pytest.mark.parametrize("provided_input", ["24-26", "100"])
    def test_invalid_hour_field(self, provided_input):
        with pytest.raises(CronFieldParsingError):
            hour_field = HourCronFieldParser(provided_input)
            hour_field.evaluateExpression()

    @pytest.mark.parametrize("provided_input", ["32", "100"])
    def test_invalid_day_of_month_field(self, provided_input):
        with pytest.raises(CronFieldParsingError):
            day_of_month_field = DayCronFieldParser(provided_input)
            day_of_month_field.evaluateExpression()

    @pytest.mark.parametrize("provided_input", ["0-8", "10-20", "100", "SUN-5"])
    def test_invalid_day_of_week_field(self, provided_input):
        with pytest.raises(CronFieldParsingError):
            day_of_week_field = WeekDayCronFieldParser(provided_input)
            day_of_week_field.evaluateExpression()

    @pytest.mark.parametrize("provided_input", ["13,15", "100", "JAN/3", "JAN-4", "1,FEB"])
    def test_invalid_month_field(self, provided_input):
        with pytest.raises(CronFieldParsingError):
            month_field = MonthCronFieldParser(provided_input)
            month_field.evaluateExpression()

    @pytest.mark.parametrize(
        "provided_input",
        [
            "*/15 8-17 * * 1-5",
            "*/10 2-9 * *",
        ],
    )
    def test_invalid_cron_expression(self, provided_input):
        with pytest.raises(CronParsingExceptionError):
            CronExpressionParser(provided_input).print_expanded_cron_expr()
