import argparse
from fpdf import FPDF
import pandas as pd
from fpdf.table import Table
from fpdf.enums import Corner, XPos, YPos
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.image("logo.png", x=10, y=8, w=92)
        self.set_font("Helvetica", size=10)
        self.set_fill_color(227, 217, 246) 
        self.rect(109, 0, 105, 34, round_corners=(Corner.BOTTOM_RIGHT,), style="F")
        self.set_text_color(0, 0, 0)
        self.image("icon.png", x=112, y=6.5, w=7)
        self.text(x=123, y=11, text="+91 7905820313")
        self.text(x=123, y=16, text="info@sequensale.online")
        self.text(x=123, y=21, text="Flexcel Park, C Wing, S.V. Road, Jogeshwari(W),")
        self.text(x=123, y=26, text="Mumbai 400102, Maharashtra, India.")
        self.image("watermark.png", x=13, y=25, w=190)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', "I", 8)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, "Business Confidential", align='C')

    def add_table(self, df, col_widths):
        rows = [list(df.columns)] + df.astype(str).values.tolist()
        self.set_text_color(0, 0, 0)
        self.font_size = 8
        self.set_font("Helvetica", size=8)
        with self.table(col_widths=col_widths, line_height=self.font_size, padding=2.5,text_align=("LEFT", "CENTER", "CENTER", "CENTER", "CENTER", "CENTER")) as table:
            for row in rows:
                table.row(row)

    def create_pdf_table(file_path, output_pdf_path, date):
        df = pd.read_csv(file_path)
        df['#Q20 Bases'] = [f"{float(i.split('(')[1].split(')')[0].replace('%','')):.2f}%" for i in df["#Q20 Bases"]]
        df['#Q30 Bases'] = [f"{float(i.split('(')[1].split(')')[0].replace('%','')):.2f}%" for i in df["#Q30 Bases"]]
        df = df[['Sample Id', '#Reads', 'Read Mean Length', '#Q20 Bases', '#Q30 Bases', str('%GC')]] 
        df = df.sort_values(by='Sample Id').reset_index(drop=True)

        col_widths = [80, 20, 20, 20, 20, 20]
        pdf = PDF()
        pdf.add_page()
        pdf.set_margins(left=12, top=44, right=12)
        pdf.set_font("Helvetica", "B", size=22)
        pdf.set_text_color(101, 44, 145)
        pdf.cell(0, 12, "Raw Read Statistics Report")
        pdf.ln(10)
        pdf.set_font("Helvetica", style="B", size=12)
        pdf.write(10, "Date : ")
        pdf.set_font("Helvetica", size=12)
        pdf.set_text_color(0, 0, 0)
        pdf.write(10, date)
        pdf.ln(5)
        # pdf.image("line.png", x=0.7, y=59, w=211)
        pdf.set_line_width(0.5)
        pdf.set_draw_color(101, 38, 137)
        pdf.line(12, 65, 198, 65)
        pdf.ln(15)
        pdf.set_font("Helvetica", size=8)
        pdf.add_table(df, col_widths)
        pdf.ln(25)

        right_x = 123
        current_y = pdf.get_y()
        pdf.set_x(right_x)
        pdf.set_font("Helvetica", style="B", size=12)
        pdf.set_text_color(101, 44, 145)
        pdf.cell(0, 5, "Thank you.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_x(right_x)
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 5, "SequenSale®", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_x(right_x)
        pdf.set_font("Helvetica", size=10)
        pdf.cell(0, 5, "Flexcel Park, C Wing, S.V. Road, Jogeshwari(W),", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_x(right_x)
        pdf.cell(0, 5, "Mumbai 400102, Maharashtra, India.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.output(output_pdf_path)
        print("PDF with table created:", output_pdf_path)

# -------------------- argparse CLI ---------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PDF Report from CSV")
    parser.add_argument("-i", "--input", default="epigeneres.csv", help="Path to the input CSV file")
    parser.add_argument("-d", "--date", help="Optional date for the report (format: DD-MM-YYYY)")
    args = parser.parse_args()

    file_path = args.input
    date = args.date if args.date else datetime.today().strftime("%d-%m-%Y")

    output_pdf_path = "RawReadTable.pdf"

    PDF.create_pdf_table(file_path, output_pdf_path, date)
