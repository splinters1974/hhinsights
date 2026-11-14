"""
Makes the made-up sample files in site/samples/. Seeded, so the files (and
the figures quoted from them in the worked examples) are reproducible.

    python3 tools/make_samples.py
"""
import datetime as dt
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'site' / 'samples'
BH = {'2024-05-06', '2024-05-27', '2024-08-26', '2024-12-25', '2024-12-26', '2025-01-01'}


def days(start, n):
    d = dt.date.fromisoformat(start)
    return [d + dt.timedelta(k) for k in range(n)]


def season(d):  # winter higher
    return 1 + 0.18 * math.cos((d.timetuple().tm_yday - 15) / 365 * 2 * math.pi)


def write(name, rows):
    with open(OUT / f'{name}.csv', 'w') as f:
        f.write('Date,' + ','.join(f'HH{i:02d}' for i in range(1, 49)) + '\n')
        for d, v in rows:
            f.write(d.isoformat() + ',' + ','.join(f'{x:.2f}' for x in v) + '\n')


def profile(d, base, peak, start, end, open_day, r):
    v = []
    for s in range(48):
        h = s / 2
        kw = (peak if open_day and start <= h < end else base) * season(d)
        if open_day and (start - 1 <= h < start or end <= h < end + 1):
            kw = (base + peak) / 2 * season(d)
        v.append(max(0, kw * (1 + r.gauss(0, 0.06))) * 0.5)
    return v


def office():
    """A small office, mostly weekdays 07:30-18:30, in about half the Saturdays."""
    r = random.Random(7)
    write('example-office', [(d, profile(d, 3.2, 18, 7.5, 18.5, d.weekday() < 5 or (d.weekday() == 5 and r.random() < .5), r))
                             for d in days('2024-04-01', 365)])


def school():
    """A primary school, 08:00-16:30 in term. Heating plant left on through
    October half term; the hall let on Tuesday and Thursday evenings in term."""
    r = random.Random(11)
    holidays = [('2024-04-01', '2024-04-12'), ('2024-05-27', '2024-05-31'), ('2024-07-22', '2024-09-03'),
                ('2024-10-28', '2024-11-01'), ('2024-12-23', '2025-01-03'), ('2025-02-17', '2025-02-21')]
    half_term = ('2024-10-28', '2024-11-01')

    def within(d, a, b):
        return a <= d.isoformat() <= b

    rows = []
    for d in days('2024-04-01', 365):
        holiday = any(within(d, a, b) for a, b in holidays) or d.isoformat() in BH
        term_day = d.weekday() < 5 and not holiday
        v = profile(d, 2.4, 21, 8, 16.5, term_day, r)
        if within(d, *half_term) and d.weekday() < 5:
            # Plant ran to the term-time schedule with nobody in.
            v = [x + (8 * season(d) * 0.5 if 7 <= s / 2 < 17 else 0) for s, x in enumerate(v)]
        if term_day and d.weekday() in (1, 3):
            # Evening hall let 18:00-21:00: the whole ground floor lit and heated.
            v = [x + (6 * season(d) * 0.5 if 18 <= s / 2 < 21 else 0) for s, x in enumerate(v)]
        rows.append((d, v))
    write('example-school', rows)


if __name__ == '__main__':
    office()
    school()
    print('wrote', ', '.join(p.name for p in sorted(OUT.glob('*.csv'))))
