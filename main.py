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
- Media italiana 0.234 kgCO2/kWh
- Lombardia 0.202 kgCO2/kWh
- Lazio 0.291 kgCO2/kWh
Per Lione considero la media francese di 0.052 kgCO2/kWh (valore ADEME)

Per il gasolio considero il fattore di emissione riportato nel link sotto, ovvero 2.620 kgCO2/litro
https://natural-resources.canada.ca/sites/nrcan/files/oee/pdf/transportation/fuel-efficient-technologies/autosmart_factsheet_9_e.pdf

Per il gas naturale (metano) considero i fattori di emissione dei coefficienti standard nazionali, 
pari a 2,019 tCO2/1000stdm3 --> 0.002 kgCO2/sm3
https://www.ets.minambiente.it/Download/237/Tabella%20coefficienti%20standard%20nazionali%202021-2023_v1.pdf
'''

# CREO UN DATAFRAME CON I FATTORI DI EMISSIONE (kgCO2)

fattori_emissione = pd.DataFrame([{'Risorsa': 'Elettricità', 'Città': 'Milano', 'Fattore emissione (kgCO2)': 0.202},
                                  {'Risorsa': 'Elettricità', 'Città': 'Roma',
                                   'Fattore emissione (kgCO2)': 0.291},
                                  {'Risorsa': 'Elettricità', 'Città': 'Lione',
                                   'Fattore emissione (kgCO2)': 0.052},
                                  {'Risorsa': 'Gas Naturale', 'Città': 'Milano',
                                   'Fattore emissione (kgCO2)': 0.002},
                                  {'Risorsa': 'Gas Naturale', 'Città': 'Roma',
                                   'Fattore emissione (kgCO2)': 0.002},
                                  {'Risorsa': 'Gas Naturale', 'Città': 'Lione',
                                   'Fattore emissione (kgCO2)': 0.002},
                                  {'Risorsa': 'Gasolio', 'Città': 'Milano',
                                   'Fattore emissione (kgCO2)': 2.620},
                                  {'Risorsa': 'Gasolio', 'Città': 'Roma',
                                   'Fattore emissione (kgCO2)': 2.620},
                                  {'Risorsa': 'Gasolio', 'Città': 'Lione', 'Fattore emissione (kgCO2)': 2.620}])

# AGGIUNGO FATTORI DI EMISSIONE AL DATAFRAME
df = pd.merge(df, fattori_emissione)

# CALCOLO EMISSIONI
df['Emissioni (kgCO2)'] = (
    df['Quantità']*df['Fattore emissione (kgCO2)']).round(decimals=2)
print(df)
