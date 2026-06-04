import pandas as pd

# IMPORTO EXCEL
data_lione = pd.read_excel(
    'ESG-Data-Automation-Validation\data\consumi_lione.xlsx')
data_milano = pd.read_excel(
    'ESG-Data-Automation-Validation\data\consumi_milano.xlsx')
data_roma = pd.read_excel(
    'ESG-Data-Automation-Validation\data\consumi_roma.xlsx')

# AGGIUNGO CATEGORIA CITTA'
data_lione['Città'] = 'Lione'
data_milano['Città'] = 'Milano'
data_roma['Città'] = 'Roma'

# UNISCO I DATAFRAME
df = pd.concat([data_lione, data_milano, data_roma])

# CONVERSIONE TESTO
df['Unità'] = df['Unità'].str.lower()
df['Categoria'] = df['Categoria'].str.title()
df['Risorsa'] = df['Risorsa'].str.title()

# ELIMINO LE RIGHE VUOTE IN QUANTITA'= NaN
df = df.dropna(subset=['Quantità'])

# SISTEMO FORMATTAZIONE DATE
df['Data'] = pd.to_datetime(
    df['Data'], dayfirst=True, format='mixed').dt.strftime('%d/%m/%Y')

# SORT BY CATEGORIA
df = df.sort_values(by='Categoria')

# FATTORI DI EMISSIONE
''' I fattori di emissioni sono presi dal documento ISPRA reperibile nel link sotto
https://www.isprambiente.gov.it/files2025/pubblicazioni/rapporti/r413-2025_def.pdf#page=15.26

I dati presi in considerazione sono i fattori di emissione (FE) di consumo regionali del 2023:
- Media italiana 234.7 gCO2/kWh
- Lombardia 202.2 gCO2/kWh
- Lazio 291.2 gCO2/kWh
Per Lione considero la media francese di 52 gCO2/kWh (valore ADEME)

Per il gasolio considero il fattore di emissione riportato nel link sotto, ovvero 2.7 kgCO2/litro
https://natural-resources.canada.ca/sites/nrcan/files/oee/pdf/transportation/fuel-efficient-technologies/autosmart_factsheet_9_e.pdf

Per il gas naturale (metano) considero i fattori di emissione dei coefficienti standard nazionali, 
pari a 2,019 tCO2/1000stdm3 --> 2,019 gCO2/sm3
https://www.ets.minambiente.it/Download/237/Tabella%20coefficienti%20standard%20nazionali%202021-2023_v1.pdf
'''
fattori_emissione = {'en_italia': 234.7,
                     'en_lombardia': 202.2,
                     'en_lazio': 291.2,
                     'en_francia': 52,
                     'gasolio': 2700,
                     'metano': 2.019}
