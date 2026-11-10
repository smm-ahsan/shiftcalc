# ShiftCalc

A tiny, dependency-free command line tool that calculates worked hours
and gross pay from your shift times.

Tell it your hourly rate and your shifts for the week, and it prints the
paid hours and gross pay for each shift plus the week total.

## Why

Shift workers in kitchens, shops, hotels and care work often get paid by
the hour against a rota, and payslips are not always easy to follow. If
you worked a week of evenings, you should be able to check in ten seconds
that the hours and the gross pay on your payslip match the shifts you
actually did. ShiftCalc is that check: no spreadsheet, no sign-up, no
app, just your shifts and your rate.

## Features

- Zero dependencies - pure Python 3 standard library
- Any number of shifts per run, one flag per shift
- **Overnight shifts handled correctly**: a shift ending at or before
  its start time runs into the next day, so `18:00-00:30` counts as
  6.5 hours
- `24:00` accepted as an end time for shifts that finish at midnight
- Optional unpaid break deducted per shift (`--break-minutes`)
- Clear errors and exit code 2 on bad input, so it is safe in scripts

## Install

No installation needed. Clone the repo and run it with Python 3:

```bash
git clone https://github.com/ahsanhani/shiftcalc.git
cd shiftcalc
python3 shiftcalc.py --help
```

## Usage

One shift:

```bash
python3 shiftcalc.py --rate 10 --shift "Mon 18:00-24:00"
```

A full week with a 30 minute unpaid break per shift:

```bash
python3 shiftcalc.py --rate 10 \
  --shift "Mon 18:00-24:00" \
  --shift "Tue 18:00-00:30" \
  --shift "Wed 09:00-17:00" \
  --break-minutes 30
```

Output:

```
Mon: 5.50 hours, pay 55.00
Tue: 6.00 hours, pay 60.00
Wed: 7.50 hours, pay 75.00
Total hours: 19.00
Total gross pay: 190.00
```

Note the Tuesday shift: 18:00 to 00:30 is 6.5 hours because it runs
past midnight, and minus the 30 minute break it pays 6.00 hours.

See [examples.md](examples.md) for more sample runs.

## Roadmap

- Read shifts from a plain text file or CSV rota
- Different rates for nights, Sundays and public holidays
- Overtime rate after a weekly hours threshold
- Print a simple weekly summary table

## Contributing

Issues and pull requests are welcome. If you work shifts and your rota
has a pattern the tool gets wrong (split shifts, on-call, anything odd),
open an issue with an example week.

## License

MIT - see [LICENSE](LICENSE).
