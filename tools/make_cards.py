"""
Typographic guide cards for pages that don't have designed artwork yet, in the
same palette and layout as the designed cards: teal panel, white title, lime
rule. A stylised day of half-hourly demand fills the space a photo would.

    python3 tools/make_cards.py

Writes site/images/guides/<page>.jpg (1200 x 630) and <page>-600.jpg. To use
designed artwork instead, replace those two files and remove the page here.
Needs Pillow and the DejaVu Sans Bold font.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

CARDS = {
    'half-hourly-data-british-gas': 'Half-hourly data from British Gas Business',
    'half-hourly-data-edf': 'Half-hourly data from EDF',
    'half-hourly-data-eon-next': 'Half-hourly data from E.ON Next',
    'half-hourly-data-npower-business-solutions': 'Half-hourly data from npower Business Solutions',
    'half-hourly-data-totalenergies': 'Half-hourly data from TotalEnergies',
    'mpan-profile-class': 'Reading your MPAN',
    'electricity-benchmarks': 'Electricity benchmarks by sector',
}

TEAL, LIME, WHITE = (3, 52, 59), (181, 247, 53), (255, 255, 255)
BAR, BAR_HI = (24, 92, 104), (0, 101, 164)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
OUT = os.path.join(os.path.dirname(__file__), '..', 'site', 'images', 'guides')
W, H = 1200, 630


def wrap(draw, text, font, width):
    lines, line = [], ''
    for word in text.split():
        trial = f'{line} {word}'.strip()
        if draw.textlength(trial, font=font) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def card(name, title):
    rnd = random.Random(name)            # same picture every time for the same page
    im = Image.new('RGB', (W, H), TEAL)
    d = ImageDraw.Draw(im)
    # A day of demand: low overnight, a working-day block, a few late spikes.
    base, top = 470, 190
    for i in range(48):
        h = 0.18 + (0.62 if 15 <= i < 37 else 0) * (0.85 + 0.15 * math.sin(i / 3)) + rnd.random() * 0.08
        x = 60 + i * 23
        y = base + 120 - int(h * (base - top + 120))
        d.rectangle([x, y, x + 15, base + 120], fill=BAR_HI if 15 <= i < 37 else BAR)
    d.rectangle([0, 0, W, 330], fill=TEAL)  # keep the title area clear
    size = 64
    font = ImageFont.truetype(FONT, size)
    lines = wrap(d, title, font, 1000)
    while len(lines) > 3:
        size -= 6
        font = ImageFont.truetype(FONT, size)
        lines = wrap(d, title, font, 1000)
    y = 70
    for line in lines:
        d.text((64, y), line, font=font, fill=WHITE)
        y += int(size * 1.2)
    d.rectangle([64, y + 18, 264, y + 28], fill=LIME)
    im.save(os.path.join(OUT, f'{name}.jpg'), quality=85, optimize=True, progressive=True)
    im.resize((600, 315), Image.LANCZOS).save(os.path.join(OUT, f'{name}-600.jpg'), quality=82, optimize=True, progressive=True)


if __name__ == '__main__':
    for name, title in CARDS.items():
        card(name, title)
    print(f'wrote {len(CARDS)} cards')
