from sys import argv

from cron_base_class import (
    DayCronFieldParser,
    HourCronFieldParser,
    MinuteCronFieldParser,
    MonthCronFieldParser,
    WeekDayCronFieldParser,
)


class CronParsingExceptionError(Exception):
    code = "invalid Cron Expression"


class CronExpressionParser:

    def __init__(self, cron_expression):
        self.cron_expression = cron_expression

    def split_cron_expression(self):
        try:
            minute, hour, day, month, week_day, command = self.cron_expression.split(' ', 5)
        except ValueError:
            raise CronParsingExceptionError("Insufficient numbers of parameters passed.")

        minute = MinuteCronFieldParser(minute)
        hour = HourCronFieldParser(hour)
        day = DayCronFieldParser(day)
        month = MonthCronFieldParser(month)
        week_day = WeekDayCronFieldParser(week_day)

        return minute, hour, day, month, week_day, command

    def describe_cron_expr(self):
        minute, hour, day, month, week_day, command = self.split_cron_expression()
        return '\n'.join([
            f"minute        {minute.evaluateExpression()}",
            f"hour          {hour.evaluateExpression()}",
            f"day of month  {day.evaluateExpression()}",
            f"month         {month.evaluateExpression()}",
            f"day of week   {week_day.evaluateExpression()}",
            f"command       {command}",
        ])

    def print_expanded_cron_expr(self):
        print(self.describe_cron_expr())


if __name__ == "__main__":
    if len(argv) < 2:
        raise CronParsingExceptionError("Invalid expression provided to parse")
    cron_expr_parser = CronExpressionParser(argv[1])
    cron_expr_parser.print_expanded_cron_expr()