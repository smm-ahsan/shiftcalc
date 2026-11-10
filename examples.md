# Examples

Real output from ShiftCalc, captured from an actual run.

## A week of kitchen shifts with a 30 minute unpaid break

Command:

```bash
python3 shiftcalc.py --rate 10 --shift "Mon 18:00-24:00" --shift "Tue 18:00-00:30" --shift "Wed 09:00-17:00" --break-minutes 30
```

Output:

```
Mon: 5.50 hours, pay 55.00
Tue: 6.00 hours, pay 60.00
Wed: 7.50 hours, pay 75.00
Total hours: 19.00
Total gross pay: 190.00
```

How each shift is worked out:

- **Mon 18:00-24:00** is 6 hours, minus the 30 minute break = 5.50 paid hours.
- **Tue 18:00-00:30** runs past midnight, so it is 6.5 hours, minus the break = 6.00 paid hours.
- **Wed 09:00-17:00** is 8 hours, minus the break = 7.50 paid hours.

Total paid time is 19.00 hours, and at a rate of 10 per hour the gross pay is 190.00.
