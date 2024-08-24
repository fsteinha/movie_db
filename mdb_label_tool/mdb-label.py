import sys
import argparse

sys.path.append('../')
from mdb.mdb_xlsx import CMdbXlsx
from pdf.pdf_table import create_pdf_table

KEY_TYPE_XLSX = "xlsx-google"

def main():
    args = parse_arg()

    if args.type == KEY_TYPE_XLSX:
        xlsx_proceed(args.database)

def xlsx_proceed(database, columns=4):
    db = CMdbXlsx(database)
    db.read()
    d_box = db.sort_box_oriented_titles()

    for box in d_box.keys():
        table = []
        pdf_title = f"box_{box}"
        count = 0
        for title in d_box[box]:
            if count == 0:
                row = []

            if count < columns:
                row.append(title)
                count += 1
            else:
                table.append(row)
                count = 0
        
       # print(table)
        
        create_pdf_table(f"{pdf_title}.pdf", table, f"Box {str(box)}")

def parse_arg() ->argparse.Namespace:
    parser = argparse.ArgumentParser(description='Create labels for each bos',
                                     epilog='Text at the bottom of help')
    
    parser.add_argument('database', help="Path to database. The type is given by the type option")
    parser.add_argument('-t', '--type', default=KEY_TYPE_XLSX, choices=['xlsx-google'], help="type of database (%(default)s)")
    return parser.parse_args()

if __name__ == "__main__":
    main()