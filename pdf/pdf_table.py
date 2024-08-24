from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def create_pdf_table(filename, table_data, headline, fontsize = 6):
    pdf_canvas = canvas.Canvas(filename, pagesize=landscape(A4))
    
    # calc col widths
    col_widths = [int(max([len(str(item)) for item in col]) * (fontsize/1.6)) for col in zip(*table_data)]
    #table
    table = Table(table_data, colWidths=col_widths, rowHeights=[None] * len(table_data))
    
    style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), fontsize),  # font size header
        ('FONTSIZE', (0, 1), (-1, -1), fontsize),  # font size rest
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table_width, table_height = table.wrap(0, 0)
    
    # Setze die Headline genau über die Tabelle
    headline_y_position = 50 + table_height + 20  # 20 Einheiten Abstand zur Tabelle
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(50, headline_y_position, headline)

    table.setStyle(style)
    #table.wrapOn(pdf_canvas, 400, 200)
    table.drawOn(pdf_canvas, 50, 50)
    pdf_canvas.save()

