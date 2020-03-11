import csv
import glob
import os
import pprint
import xml.etree.ElementTree as ET
from typing import Any, List

YEARS = ['2002', '2004', '2006', '2008', '2010', '2014', '2016']

def get_list_files_by_year(year: str) -> List[str]:        
    list_files = [f for f in glob.glob(year + '/*')]
    return list_files

def get_data_file(year: str, file_name: str) -> Any:
    root = ET.parse(file_name).getroot()
    id_grup = root.attrib['NRO-ID-GRUPO']
    year_census = root.attrib['ANO-CENSO']
    list_area = [f.attrib['AREA-PROGRAMA'] for f in root.iter('DOCENTE-PROGRAMA')]
    list_big_area = [f.attrib['GRANDE-AREA-PROGRAMA'] for f in root.iter('DOCENTE-PROGRAMA')]
    try:
        list_cnpj = [f.attrib['SUB-CNPJ'] for f in root.iter('EMPRESA')]
    except:
        pass
    try:
        list_cnpj = [f.attrib['CNPJ'] for f in root.iter('EMPRESA')]
    except:
        pass
    
    try:
        list_employe = [f.attrib['FAIXA-FUNCIONARIOS'] for f in root.iter('EMPRESA')]
    except:
        list_employe = []
    list_company_nature = [f.attrib['NATUREZA-JURIDICA'] for f in root.iter('EMPRESA')]
    list_company_name = [f.attrib['NOME-DA-EMPRESA'] for f in root.iter('EMPRESA')]

    data_file = [id_grup, year_census]

    data_file.extend(list_area+list_big_area+list_cnpj+list_employe+list_company_nature+list_company_name)
    return data_file

with open('censo.csv', 'w') as csv_file, open('erro.txt', 'w') as log:
    writer = csv.writer(csv_file, delimiter ='|',quotechar =',',quoting=csv.QUOTE_MINIMAL)
    for year in YEARS:
        list_files = get_list_files_by_year(year)

        for file in list_files:
            try:
                data_file = get_data_file(year, file)
                writer.writerow(data_file)
            except Exception as e:
                print(e)
                log.write(file + '\n')

            
        
        
