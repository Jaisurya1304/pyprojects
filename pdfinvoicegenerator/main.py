import glob
import pandas as pd
from fpdf import FPDF
from pathlib import Path

fps = glob.glob("Invoices/*.xlsx")
for fp in fps:

    pdf = FPDF(orientation="P", unit="mm", format="a4")
    pdf.add_page()

    filename = Path(fp).stem
    in_nr, date = filename.split('-')

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Invoice no:{in_nr}", ln=1)

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Date:{date}", ln=1)

    df = pd.read_excel(fp, sheet_name="Sheet 1")

    columns=list(df.columns)
    pdf.set_font(family="Times", size=10, style="B")
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt=columns[0], ln=0, border=1)
    pdf.cell(w=70, h=8, txt=columns[1], ln=0, border=1)
    pdf.cell(w=30, h=8, txt=columns[2], ln=0, border=1)
    pdf.cell(w=30, h=8, txt=columns[3], ln=0, border=1)
    pdf.cell(w=30, h=8, txt=columns[4], ln=1, border=1)
    for index, row in df.iterrows():
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)

        pdf.cell(w=30,h=8,txt=str(row["product_id"]),ln=0,border=1)
        pdf.cell(w=70, h=8, txt=str(row["product_name"]), ln=0,border=1)
        pdf.cell(w=30, h=8, txt=str(row["amount_purchased"]), ln=0,border=1)
        pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), ln=0,border=1)
        pdf.cell(w=30, h=8, txt=str(row["total_price"]), ln=1,border=1)

    total_sum=df["total_price"].sum()
    pdf.cell(w=30, h=8, txt="", ln=0, border=1)
    pdf.cell(w=70, h=8, txt="", ln=0, border=1)
    pdf.cell(w=30, h=8, txt="", ln=0, border=1)
    pdf.cell(w=30, h=8, txt="", ln=0, border=1)
    pdf.cell(w=30, h=8, txt=str(total_sum), ln=1, border=1)

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"The total amount is {total_sum}!!", ln=1)
    pdf.output(f"{filename}.pdf")
