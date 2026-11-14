"""
Makes site/downloads/half-hourly-data-request.docx: an editable letter or
email asking an electricity supplier for half-hourly data. Needs python-docx.

    python3 tools/make_letter.py
"""
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor

OUT = Path(__file__).resolve().parent.parent / 'site' / 'downloads' / 'half-hourly-data-request.docx'
INK = RGBColor(0x06, 0x3C, 0x55)

# Kept in step with the request shown on get-your-data.html.
LETTER = [
    '[Your organisation]\n[Address]',
    '[Date]',
    '[Supplier name]\nCustomer services / Account manager',
    'Request for half-hourly electricity consumption data',
    'Account number: [account number]',
    'Dear Sir or Madam,',
    'Please send us the half-hourly electricity consumption data for the meters listed below, for the period from [start date] to [end date], or for as much of the last three years as you hold.',
    'For each meter, please provide:',
    '• consumption in kWh for every half hour;\n• one file per meter, in Excel or CSV format;\n• ideally one row per day with 48 half-hourly columns, though one row per reading with its date and time is also fine.',
    'Meters (MPAN, the 13-digit supply number on our bills):\n[MPAN 1] – [site name]\n[MPAN 2] – [site name]',
    'If any of these meters is not read half-hourly, please let us know, along with the readings you do hold.',
    'Please send the files to [email address]. If you need anything further to process this request, contact [name] on [phone number].',
    'Yours faithfully,',
    '[Name]\n[Job title]',
]


def main():
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(11)
    for i, text in enumerate(LETTER):
        p = doc.add_paragraph()
        run = p.add_run(text)
        if text.startswith('Request for half-hourly'):
            run.bold = True
            run.font.size = Pt(13)
            run.font.color.rgb = INK
    doc.core_properties.title = 'Request for half-hourly electricity consumption data'
    doc.core_properties.author = 'Half Hourly Insights'
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print('wrote', OUT.name)


if __name__ == '__main__':
    main()
