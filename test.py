import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos

pdf = FPDF()
pdf.set_margins(left=15, top=15, right=15)
pdf.add_page()
pdf.set_font("Helvetica", size=10)

pdf.set_font("Helvetica", style="B", size=12)
pdf.write(10, "Powered ")
pdf.set_font("Helvetica", style="", size=12)
pdf.write(10, "by FPDF.")

pdf.set_font("Helvetica", "B", 10)
pdf.cell(w=20, h=10, text="DATE :", new_x=XPos.RIGHT, new_y=YPos.TOP)  # ln=0 = stay on same line

# Normal "04/06/2025"
pdf.set_font("Helvetica", "", 10)
pdf.cell(w=0, h=10, text="04/06/2025", new_x=XPos.LMARGIN, new_y=YPos.NEXT) 

# Load and clean the CSV data with pandas
df = pd.read_csv("genepowerdx - genepowerdx.csv")

# Clean the #Q20 Bases and #Q30 Bases columns
df['#Q20 Bases'] = df['#Q20 Bases'].apply(lambda x: x.split('(')[1].split(')')[0])
df['#Q30 Bases'] = df['#Q30 Bases'].apply(lambda x: x.split('(')[1].split(')')[0])

# Select and sort columns
df = df[['Id', '#Reads', 'Read Mean Length', '#Q20 Bases', '#Q30 Bases', '%GC']]
df = df.sort_values(by='Id').reset_index(drop=True)

# Convert to list of rows (including header)
rows = [list(df.columns)] + df.astype(str).values.tolist()

# Set custom widths (6 columns = must match your column count)
col_widths = [60, 25, 25, 25, 25, 20]

with pdf.table(col_widths=col_widths) as table:
    for row in rows:
        table.row(row)

pdf.ln(20)  # Add space after table
right_x = 123
current_y = pdf.get_y()

pdf.set_xy(right_x, current_y + 10)

pdf.set_font("Helvetica", style="B", size=12)
pdf.set_text_color(101, 44, 145)
pdf.cell(0, 5, "Thank you.", new_x=XPos.RMARGIN, new_y=YPos.NEXT)

pdf.set_x(right_x)
pdf.set_font("Helvetica", style="B", size=10)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 5, "SequenSale®", new_x=XPos.RMARGIN, new_y=YPos.NEXT)

pdf.set_x(right_x)
pdf.set_font("Helvetica", size=10)
pdf.cell(0, 5, "Flexcel Park, C Wing, S.V. Road, Jogeshwari(W),", new_x=XPos.RMARGIN, new_y=YPos.NEXT)

pdf.set_x(right_x)
pdf.cell(0, 5, "Mumbai 400102, Maharashtra, India.", new_x=XPos.RMARGIN, new_y=YPos.NEXT)
pdf.output("raw.pdf")
