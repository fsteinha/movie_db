
#!/usr/bin/python3

import sys
import argparse
import re

sys.path.append('../')
from mdb.mdb_xlsx import CMdbXlsx
from pdf.pdf_table import create_pdf_table
import json

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, PageBreak 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, _baseFontName, _baseFontNameB, _baseFontNameI 
from reportlab.lib import colors 
from reportlab.lib.units import mm # Importiere mm
#from reportlab.rl_config import canvas_basefontname as _baseFontName
from PIL import Image as PilImage
from io import BytesIO
from datetime import datetime

KEY_TYPE_XLSX = "xlsx-google"

def main():
    '''Main function'''
    args = parse_arg()

    if args.type == KEY_TYPE_XLSX:
        xlsx_proceed(args.database, args.path, args.columns)
    else:
        raise Exception (f"Not supported {args.type}")
    

def xlsx_proceed(database, path2images, columns=4):
    db = CMdbXlsx(database)
    data = db.read()
    with open("test.json", "w") as file:
        json.dump(data, file, indent=4)
    
    # make pdf 
    pdf = SimpleDocTemplate("Filmkatalog.pdf", pagesize=A4)

    # make table data
    table_data = [["Title", "Box", "Foto", "Beschreibung"]]
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='NewNormal',
                              fontName=_baseFontName,
                              fontSize=8,
                              leading=12)
                   )

    styles.add(ParagraphStyle(name='NewNormalB',
                              fontName=_baseFontNameB,
                              fontSize=8,
                              leading=12)
                   )

    styles.add(ParagraphStyle(name='NewNormalI',
                              fontName=_baseFontNameI,
                              fontSize=8,
                              leading=12)
                   )

    count =  len(data.items())- 1 # reduce by "index" entry     
    for title in data['Index']:
        for index in data['Index'][title]:
            s_description = data[index]['Description']
            if type(s_description) == str:
                s_description = f"{get_first_words(s_description, 15)} ..."
                description = Paragraph(s_description, styles["NewNormal"])
            else:
                description = "N/A"

            poster = data[index]['Poster']
            if (type(poster) == str):
                posters = data[index]['Poster'].split(", ")
            else:
                posters = []
            
            image = "N/A"
            for poster in posters:
                if (poster.find("file:") != -1):
                    path = path2images + "/" + poster.split("/")[-1]
                    image = Image(convert_image2thumbnail(path, 50, 75))
            
            short_info = [Paragraph(data[index]["Title"], styles["NewNormalB"]), 
                          Paragraph(get_first_words(str(data[index]["Genres"]), 10), styles["NewNormalI"]),
                          Paragraph(get_first_words(get_actor_string(str(data[index]["Actors"])), 10), styles["NewNormal"])]
            

            row = [short_info, data[index]["box"], image, description]
            table_data.append(row)


    table = Table(table_data, colWidths=[2.5*inch, 1.0*inch, 1.5*inch, 2.0*inch]) 
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey), 
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), 
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), 
        ('ALIGN', (0, 1), (0, -1), 'LEFT'), 
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), 
        ('FONTSIZE', (0, 0), (-1, -1), 8), 
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8), 
        ('BACKGROUND', (0, 1), (-1, -1), colors.white), 
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP') 
        ]))    
    
    elements = []
    current_date = datetime.now().strftime("%d.%m.%Y")
    elements.append(Paragraph(f"Filmkatalog ({current_date}, {count})", styles['Title']))
    elements.append(table) 
    
    # PDF generieren 
    pdf.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    
def convert_image2thumbnail(path, width=100, height=150): 
    image = PilImage.open(path) 
    image.thumbnail((width, height), PilImage.LANCZOS) 
    img_byte_arr = BytesIO() 
    image.save(img_byte_arr, format='PNG') 
    img_byte_arr.seek(0) 
    return img_byte_arr
    
def add_page_number(canvas, doc): 
    page_num = canvas.getPageNumber() 
    text = f"Seite {page_num}" 
    canvas.drawRightString(200 * mm, 15 * mm, text)

def get_first_words(text, number=20): 
    words = text.split() # Teilt den String in Wörter 
    first_words = words[:number] # Nimmt die ersten 20 Wörter 
    return ' '.join(first_words) # Fügt die Wörter wieder zu einem String zusammen 

def get_actor_string(input_string):
    # Dieses Regex-Muster erfasst "Schauspieler als Rolle" Paare
    pattern = r'(\w+ als \w+)'
    
    # Alle Matches aus dem String holen
    matches = re.findall(pattern, input_string)
    
    # Die Matches durch Kommata getrennt zusammenfügen
    formatted_string = ', '.join(matches)
    
    return formatted_string

def parse_arg() ->argparse.Namespace:
    parser = argparse.ArgumentParser(description='Create labels for each bos',
                                     epilog='Text at the bottom of help')
    
    parser.add_argument('database', help="Path to database. The type is given by the type option")
    parser.add_argument('-t', '--type', default=KEY_TYPE_XLSX, choices=[KEY_TYPE_XLSX], help="type of database (%(default)s)")
    parser.add_argument('-c', '--columns', default=4, type = int, help="count of columns for printed tables (%(default)s)")
    parser.add_argument('-p', '--path', default="/home/fsteinha/Downloads/Movies.files", type = str, help="path to the Fotos (%(default)s)")
    
    return parser.parse_args()

if __name__ == "__main__":
    main()