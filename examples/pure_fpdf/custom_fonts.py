from fpdf import FPDF

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.add_page()
pdf.add_font(family="Roboto", style="", fname="./custom_fonts/Roboto-Regular.ttf")
pdf.set_font("Roboto", "", 16)
pdf.text(40, 10, "Hello wrld!")

pdf.output("test_output_custom_fonts.pdf")
