
# Dizionari di standardizzazione

mappa_categorie = {
    # Energia
    'energia':            'Energia',
    'ENERGIA':            'Energia',
    'energia elettrica':  'Energia',
    'Energia elettrica':  'Energia',
    # Riscaldamento
    'riscaldamento':      'Riscaldamento',
    'RISCALDAMENTO':      'Riscaldamento',
    'riscald.':           'Riscaldamento',
    'Riscald.':           'Riscaldamento',
    'heating':            'Riscaldamento',
    'Heating':            'Riscaldamento',
    # Flotta aziendale
    'flotta aziendale':   'Flotta aziendale',
    'Flotta Aziendale':   'Flotta aziendale',
    'flotta aziend.':     'Flotta aziendale',
    'Flotta aziend.':     'Flotta aziendale',
    'FLOTTA':             'Flotta aziendale',
    'fleet':              'Flotta aziendale',
    'Fleet':              'Flotta aziendale',
    # Raffreddamento
    'raffreddamento':     'Raffreddamento',
    'RAFFREDDAMENTO':     'Raffreddamento',
    'cooling':            'Raffreddamento',
    'Cooling':            'Raffreddamento',
    # Acqua
    'acqua':              'Acqua',
    'ACQUA':              'Acqua',
    'acqua processo':     'Acqua',
    'Acqua processo':     'Acqua',
    # Rifiuti
    'rifiuti':            'Rifiuti',
    'RIFIUTI':            'Rifiuti',
    'waste':              'Rifiuti',
    'Waste':              'Rifiuti',
}

mappa_risorsa = {'Natural Gas': 'Gas Naturale'}

mappa_unita = {
    # kWh
    'kwh':         'kWh',
    'KWH':         'kWh',
    'Kwh':         'kWh',
    'kilowattora': 'kWh',
    # m3
    'm3':          'm3',
    'm³':          'm3',
    'mc':          'm3',
    'metri cubi':  'm3',
    'M3':          'm3',
    'SM3':         'm3',
    'Sm3':         'm3',
    'sm3':         'm3',
    # Litri
    'litri':       'Litri',
    'LITRI':       'Litri',
    'l':           'Litri',
    'L':           'Litri',
    'lt':          'Litri',
    # kg
    'kg':          'kg',
    'KG':          'kg',
    'Kg':          'kg',
    'chilogrammi': 'kg',
}

# Valori non validi (stringhe che vanno trattate come NaN)
valori_non_validi = ['N/D', 'nd', 'n/d', '-', '?', '', ' ', 'da definire']

# Mappa per inferire Categoria da Risorsa quando manca
mappa_risorsa_categoria = {
    'Elettricità':            'Energia',
    'Gas Naturale':           'Riscaldamento',
    'Gasolio':                'Riscaldamento',
    'Biomassa':               'Riscaldamento',
    'Gas refrigerante R410A': 'Raffreddamento',
    'Acqua di rete':          'Acqua',
    'Rifiuti speciali':       'Rifiuti',
    'Rifiuti urbani':         'Rifiuti',
}


mappa_risorsa_unita = {
    'Elettricità': 'kWh',
    'Gas Naturale': 'm3',
    'Gasolio': 'Litri',
    'Biomassa': 'kg',
    'Benzina': 'Litri',
    'Gas refrigerante R410A': 'kg',
    'Acqua di rete': 'm3',
    'Rifiuti speciali': 'kg',
    'Rifiuti urbani': 'kg'
}


# Risorse che appaiono in UNA sola categoria → autofill sicuro
lookup_categoria = {
    'Gas refrigerante R410A': 'Raffreddamento',  # solo in Raffreddamento
    'Acqua di rete':          'Acqua',            # solo in Acqua
    'Rifiuti speciali':       'Rifiuti',          # solo in Rifiuti
    'Rifiuti urbani':         'Rifiuti',          # solo in Rifiuti
    'Biomassa':               'Riscaldamento',    # solo in Riscaldamento
    'Benzina':                'Flotta aziendale',  # solo in Flotta aziendale

    # NON ci sono:
    # Elettricità → Energia o Raffreddamento → ambiguo
    # Gas Naturale → Riscaldamento o Flotta aziendale → ambiguo
    # Gasolio → Riscaldamento o Flotta aziendale → ambiguo
}
