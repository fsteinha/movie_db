# Purpose

This repository provides tools around my own movie database, which is based on the memento of for android (see R1).

# Tools
## md-label.py

### Purpose
This tool reads from the memento database (at time xlsx export, via google tables only) and generates labels for the boxes.

### Options
    python3 mdb-label.py -h

### Example
Reads from excel file "Movies(1).xlsx" and prints it with 3 columns 

    python3 mdb-label.py ~/Downloads/Movies\(1\).xlsx -c 3 

# Libs
## mdb/mdb_xlsx.py

This includes as interface reading the xlsx datatbase and give back need information.

## pdf/pdf_table.py

This include function to generate a table at a pdf.

# References
| ID | Link                         | Description      |
|----|------------------------------|------------------|
| R1 | https://mementodatabase.com/ | mememto database |