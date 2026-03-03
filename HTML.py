import sys
import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd
def date_time(table_cells):
    """
    This function returns the data and time from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    """
    This function returns the booster version from the HTML  table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out=''.join([booster_version for i,booster_version in enumerate( table_cells.strings) if i%2==0][0:-1])
    return out

def landing_status(table_cells):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out=[i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass=unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass=mass[0:mass.find("kg")+2]
    else:
        new_mass=0
    return new_mass


def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
        
    colunm_name = ' '.join(row.contents)
    
    # Filter the digit and empty names
    if not(colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name    
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(static_url, headers=headers)
# ... (rest of the code above remains the same)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})
    launch_table = tables[2]
    rows = launch_table.find_all('tr')
    
    # Get column names
    column_names = []
    for th in rows[0].find_all('th'):
        name = extract_column_from_header(th)
        if name is not None and len(name) > 0:
            column_names.append(name)
            
    # Initialize dictionary to store data
    launch_dict = dict.fromkeys(column_names)
    
    # Remove irrelevant columns from dictionary if necessary
    if 'Flight number' in launch_dict:
        del launch_dict['Flight number']

    # Initialize data list
    launch_data = []
    
    # Process rows
    for row in rows[1:]:
        cells = row.find_all('td')
        
        # Check if it's a valid data row (must have enough cells)
        # Based on the webpage, data rows usually have 6-7 cells
        if len(cells) < 5:
            continue
            
        # 1. Date and Time
        dt_list = date_time(cells[0])
        
        # 2. Booster Version
        bv = booster_version(cells[1])
        
        # 3. Payload Mass
        payload = get_mass(cells[3])
        
        # 4. Landing Status
        landing = landing_status(cells[4])
        
        # Add to data list
        launch_data.append({
            'Date': dt_list[0],
            'Time': dt_list[1],
            'Booster Version': bv,
            'Payload Mass': payload,
            'Landing Status': landing
        })

    # Create DataFrame
    df = pd.DataFrame(launch_data)
    print(df.head())