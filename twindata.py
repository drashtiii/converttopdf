import argparse
from fpdf import FPDF
import pandas as pd
from fpdf.table import Table
from fpdf.enums import Corner, XPos, YPos
from datetime import datetime
import re

class PDF(FPDF):
    def header(self):
        self.image("logo.png", x=10, y=8, w=92)
        self.set_font("Helvetica", size=10)
        self.set_fill_color(227, 217, 246) 
        self.rect(190, 0, 110, 34, round_corners=(Corner.BOTTOM_RIGHT,), style="F")
        self.set_text_color(0, 0, 0)
        self.image("icon.png", x=197, y=6.5, w=7)
        self.text(x=207, y=11, text="+91 7905820313")
        self.text(x=207, y=16, text="info@sequensale.online")
        self.text(x=207, y=21, text="Flexcel Park, C Wing, S.V. Road, Jogeshwari(W),")
        self.text(x=207, y=26, text="Mumbai 400102, Maharashtra, India.")
        self.image("watermark.png", x=67, y=15, w=156)

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
        with self.table(col_widths=col_widths, line_height=self.font_size, padding=2.5,text_align=(("LEFT",) + ("CENTER",) * 12)) as table:
            for row in rows:
                table.row(row)

    def create_pdf_table(file_path, output_pdf_path, date):
        df = pd.read_csv(file_path)

        # Normalize column names
        df.columns = df.columns.str.strip()

        # Ensure Sample Id exists
        if 'Sample Id' not in df.columns:
            raise KeyError("Missing 'Sample Id' column in CSV.")

        # Extract base Sample Id from Sample Id
        df['Base Sample Id'] = df['Sample Id'].str.extract(r"(.+)_R[12]_")[0]

        # Separate R1 and R2
        df_r1 = df[df['Sample Id'].str.contains('_R1_', na=False)].copy()
        df_r2 = df[df['Sample Id'].str.contains('_R2_', na=False)].copy()

        # Ensure required columns exist
        required_columns = ['#Reads', 'Read Mean Length', '#Q20 Bases', '#Q30 Bases', '%GC']
        for col in required_columns:
            if col not in df.columns:
                raise KeyError(f"Missing required column: {col}")

        # Clean % values
        def clean_percent_column(series):
            return [f"{float(i.split('(')[1].split(')')[0].replace('%','')):.2f}%" if '(' in i else i for i in series]

        df_r1['#Q20 Bases'] = clean_percent_column(df_r1['#Q20 Bases'])
        df_r1['#Q30 Bases'] = clean_percent_column(df_r1['#Q30 Bases'])
        df_r2['#Q20 Bases'] = clean_percent_column(df_r2['#Q20 Bases'])
        df_r2['#Q30 Bases'] = clean_percent_column(df_r2['#Q30 Bases'])

        # Rename for R1 and R2
        r1_cols = {
            '#Reads': '#Reads (R1)',
            'Read Mean Length': 'Read Mean Length (bases) (R1)',
            '#Q20 Bases': '#Q20 Bases (R1)',
            '#Q30 Bases': '#Q30 Bases (R1)',
            '%GC': '%GC (R1)'
        }
        r2_cols = {
            '#Reads': '#Reads (R2)',
            'Read Mean Length': 'Read Mean Length (bases) (R2)',
            '#Q20 Bases': '#Q20 Bases (R2)',
            '#Q30 Bases': '#Q30 Bases (R2)',
            '%GC': '%GC (R2)'
        }

        df_r1 = df_r1.rename(columns=r1_cols)
        df_r2 = df_r2.rename(columns=r2_cols)

        # Merge 
        merged = pd.merge(df_r1[['Base Sample Id'] + list(r1_cols.values())],
                          df_r2[['Base Sample Id'] + list(r2_cols.values())],
                          on='Base Sample Id', how='outer')
        
        merged = merged.rename(columns={'Base Sample Id': 'Sample Id'})

        

        # Final order
        final_columns = [
            'Sample Id',
            '#Reads (R1)', '#Reads (R2)',
            # '#Bases 2 (R1)', '#Bases 2 (R2)',
            'Read Mean Length (bases) (R1)', 'Read Mean Length (bases) (R2)',
            '#Q20 Bases (R1)', '#Q20 Bases (R2)',
            '#Q30 Bases (R1)', '#Q30 Bases (R2)',
            '%GC (R1)', '%GC (R2)'
        ]

        merged = merged[final_columns]

        # Create PDF
        col_widths = [56, 21, 21, 21, 21, 20, 20, 20, 20, 17.5, 17.5]

        pdf = PDF()
        pdf.add_page(orientation='L')
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
        pdf.set_line_width(0.5)
        pdf.set_draw_color(101, 38, 137)
        pdf.line(12, 65, 285, 65)
        pdf.ln(15)
        pdf.set_font("Helvetica", size=8)
        pdf.add_table(merged, col_widths)
        pdf.ln(25)

        # Footer note
        right_x = 206
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
