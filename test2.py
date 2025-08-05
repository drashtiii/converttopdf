from fpdf import FPDF
from fpdf.enums import Corner

pdf = FPDF()
pdf.add_page()
pdf.set_draw_color(200)

y = 10

# Use correct enum for rounded corners
pdf.rect(60, y, 33, 28, round_corners=(Corner.TOP_LEFT, Corner.BOTTOM_RIGHT), style="D")

pdf.set_fill_color(0, 255, 0)
pdf.rect(100, y, 50, 10, round_corners=(Corner.BOTTOM_RIGHT,), style="DF")

pdf.set_fill_color(255, 255, 0)
pdf.rect(160, y, 10, 10, round_corners=(Corner.TOP_LEFT, Corner.BOTTOM_LEFT), style="F")

pdf.output("round_corners_rectangles.pdf")