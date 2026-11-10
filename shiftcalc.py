#!/usr/bin/env python3
"""ShiftCalc - work out your hours and gross pay from your shift times.

A tiny, dependency-free tool for shift workers (cooks, retail,
hospitality, care, security) who want to check a payslip against the
shifts they actually worked.

Usage:
    python3 shiftcalc.py --rate 10 --shift "Mon 18:00-24:00"
    python3 shiftcalc.py --rate 12.50 --shift "Mon 18:00-24:00" \
        --shift "Tue 18:00-00:30" --break-minutes 30

Shifts that end at or before their start time are treated as overnight
shifts running into the next day, so 18:00-00:30 counts as 6.5 hours.
An end time of 24:00 is accepted.
"""

import argparse
import sys


def parse_time(text, is_end):
    """Turn 'HH:MM' into minutes since midnight. Raises ValueError."""
    parts = text.split(":")
    if len(parts) != 2:
        raise ValueError("time {!r} is not in HH:MM format".format(text))
    try:
        hours = int(parts[0])
        minutes = int(parts[1])
    except ValueError:
        raise ValueError("time {!r} has non-numeric hours or minutes".format(text))
    if minutes < 0 or minutes > 59:
        raise ValueError("time {!r} has minutes outside 00-59".format(text))
    if hours < 0 or hours > 24:
        raise ValueError("time {!r} has an hour outside 00-24".format(text))
    if hours == 24 and (minutes != 0 or not is_end):
        raise ValueError("24:00 is only valid as an end time")
    return hours * 60 + minutes


def parse_shift(text):
    """Turn 'Mon 18:00-24:00' into (day, start_minutes, end_minutes).

    An end time at or before the start time means the shift runs
    overnight, so the end is pushed into the next day.
    """
    fields = text.split()
    if len(fields) != 2:
        raise ValueError(
            "shift {!r} must look like 'Mon 18:00-24:00'".format(text))
    day, span = fields
    bounds = span.split("-")
    if len(bounds) != 2:
        raise ValueError(
            "shift {!r} must have a start and end time joined by '-'".format(text))
    start = parse_time(bounds[0], is_end=False)
    end = parse_time(bounds[1], is_end=True)
    if end <= start:
        end += 24 * 60  # overnight shift, ends the next day
    return day, start, end


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Calculate worked hours and gross pay from shift times."
    )
    parser.add_argument("--rate", type=float, required=True,
                        help="Hourly pay rate, e.g. 10 or 12.50")
    parser.add_argument("--shift", action="append", required=True,
                        metavar="'Day HH:MM-HH:MM'",
                        help="One shift, e.g. 'Mon 18:00-24:00'. "
                             "Repeat the flag for more shifts.")
    parser.add_argument("--break-minutes", type=int, default=0,
                        help="Unpaid break minutes taken per shift (default: 0)")
    args = parser.parse_args(argv)

    if args.rate < 0:
        parser.error("--rate cannot be negative")
    if args.break_minutes < 0:
        parser.error("--break-minutes cannot be negative")

    total_minutes = 0
    for raw in args.shift:
        try:
            day, start, end = parse_shift(raw)
        except ValueError as exc:
            print("error: {}".format(exc), file=sys.stderr)
            return 2
        worked = (end - start) - args.break_minutes
        if worked <= 0:
            print("error: shift {!r} leaves no paid time after the break"
                  .format(raw), file=sys.stderr)
            return 2
        total_minutes += worked
        hours = worked / 60.0
        print("{}: {:.2f} hours, pay {:.2f}".format(day, hours,
                                                    hours * args.rate))

    total_hours = total_minutes / 60.0
    print("Total hours: {:.2f}".format(total_hours))
    print("Total gross pay: {:.2f}".format(total_hours * args.rate))
    return 0


if __name__ == "__main__":
    sys.exit(main())
