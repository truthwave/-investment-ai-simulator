def add_table_to_pdf(pdf, title, summary_df):
    pdf.set_font("Noto", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align='L')
    pdf.set_font("Noto", size=10)
    for line in summary_df.to_string().split("\n"):
        pdf.cell(200, 6, txt=line, ln=True)
    pdf.ln(4)
