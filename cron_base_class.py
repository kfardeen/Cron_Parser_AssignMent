class CronFieldParsingError(Exception):
    code = "invalid_cron_field"



class BaseCronFieldParser():

    def __init__(self, value):
        self.value = value

    def expand_range(self,allowed_integer_values,allowed_text_values,field_type):
        try:
            start, end = self.value.split("-")
        except ValueError:
            raise CronFieldParsingError(f"Invalid format for {field_type} range. Range expr should be of format `start-end`")

        if start.isnumeric() != end.isnumeric():
            raise CronFieldParsingError(f"Invalid format for {field_type} range. Both start and end value of range should be of same type")

        if start.isnumeric():
            allowed_values = allowed_integer_values
        else:
            allowed_values = allowed_text_values

        try:
            start = allowed_values.index(start)
            end = allowed_values.index(end)
        except ValueError:
            raise CronFieldParsingError(f"Invalid format for {field_type} range. Invalid start/end value for range expr")

        if start > end:
            raise CronFieldParsingError(f"Invalid format for {field_type} range. {start} value should be <= {end}")

        return " ".join(allowed_integer_values[start:end+1])


    def expand_interval(self,allowed_integer_values,allowed_text_values,field_type):
        first, second = self.value.split("/")

        if not second.isnumeric():
            raise CronFieldParsingError(f"Invalid format for {field_type} interval. {second} should be an integer")

        if first == "*":
            return ' '.join(
                [str(i) for i in allowed_integer_values if int(i) % int(second) == 0]
            )

        if not first.isnumeric():
            raise CronFieldParsingError(f"Invalid format for {field_type} interval. {first} should be an integer or `*`")

        return " ".join([str(i) for i in range(int(first), int(allowed_integer_values[-1]) + 1) if i % int(second) == 0])

    def expand_list(self,allowed_integer_values,allowed_text_values,field_type):

        input_values = self.value.split(",")
        is_numeric_input = None
        expanded_values = []

        for input_value in input_values:
            if is_numeric_input is None:
                is_numeric_input = input_value.isnumeric()
            elif is_numeric_input != input_value.isnumeric():
                raise CronFieldParsingError(f"Invalid format for {field_type} list. All values of list should have the same type.")

            if input_value.isnumeric() and input_value not in allowed_integer_values:
                raise CronFieldParsingError(f"Invalid format for {field_type} list. {input_value} not in allowed integer values for {field_type}")
            elif not input_value.isnumeric():
                if input_value not in allowed_text_values:
                    raise CronFieldParsingError(f"Invalid format for {field_type} list. {input_value} not in allowed text values for {field_type}")

                input_value = allowed_integer_values[allowed_text_values.index(input_value)]

            expanded_values.append(input_value)

        return " ".join(expanded_values)

    def expand(self,allowed_integer_values,allowed_text_values,field_type):

        if self.value == "*":
            return " ".join(allowed_integer_values)

        if self.value == "?":
            return "Not Specified"

        if "-" in self.value:
            return self.expand_range(allowed_integer_values,allowed_text_values,field_type)

        if "/" in self.value:
            return self.expand_interval(allowed_integer_values,allowed_text_values,field_type)

        if "," in self.value:
            return self.expand_list(allowed_integer_values,allowed_text_values,field_type)

        if (
                (self.value.isnumeric() and self.value in allowed_integer_values)
                or self.value in allowed_text_values
        ):
            return self.value

        raise CronFieldParsingError(f"Unable to parse {field_type} field - {self.value}")


class MinuteCronFieldParser(BaseCronFieldParser):
    def evaluateExpression(self):
        field_type = "minute"
        allowed_integer_values = [str(i) for i in range(0, 60)]
        return BaseCronFieldParser.expand(self,allowed_integer_values,[],field_type)


class HourCronFieldParser(BaseCronFieldParser):
    def evaluateExpression(self):
        field_type = "hour"
        allowed_integer_values = [str(i) for i in range(0, 24)]
        return BaseCronFieldParser.expand(self,allowed_integer_values,[],field_type)


class DayCronFieldParser(BaseCronFieldParser):
    def evaluateExpression(self):
        field_type = "day"
        allowed_integer_values = [str(i) for i in range(0, 32)]
        return BaseCronFieldParser.expand(self,allowed_integer_values,[],field_type)


class WeekDayCronFieldParser(BaseCronFieldParser):
    def evaluateExpression(self):
        field_type = "weekday"
        allowed_integer_values = [str(i) for i in range(0, 7)]
        allowed_text_values = [
            "SUN",
            "MON",
            "TUE",
            "WED",
            "THU",
            "FRI",
            "SAT",
        ]
        return BaseCronFieldParser.expand(self,allowed_integer_values,allowed_text_values,field_type)

class MonthCronFieldParser(BaseCronFieldParser):
    def evaluateExpression(self):
        field_type = "month"
        allowed_integer_values = [str(i) for i in range(1, 13)]
        allowed_text_values = [
            "JAN",
            "FEB",
            "MAR",
            "APR",
            "MAY",
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
        ]
        return BaseCronFieldParser.expand(self,allowed_integer_values,allowed_text_values,field_type)

