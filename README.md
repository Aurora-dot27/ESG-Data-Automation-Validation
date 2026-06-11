# ESG Data Automation — GHG Emissions Reporting

A Python data pipeline that ingests raw energy consumption files from multiple production facilities, validates and cleans the data, computes greenhouse gas (GHG) emissions per the GHG Protocol, and exports a formatted multi-sheet Excel report ready for sustainability disclosure.

The project simulates a realistic corporate scenario: three plant managers submit separate Excel files with inconsistent formats, typos, and missing values. The pipeline makes the data reliable before any environmental metric is calculated — because errors in source data propagate silently into emission totals unless caught explicitly.

---

## Data Pipeline Architecture

The pipeline follows a standard ETL structure across four phases.

### Phase 1 — Data Ingestion & Exploration

The three raw facility files (`consumi_milano.xlsx`, `consumi_lione.xlsx`, `consumi_roma.xlsx`) are loaded and assessed before any transformation is applied. The initial inspection covers shape, data types, missing value percentages, and raw sample rows. An automated **Sweetviz** HTML report is generated for each file on first run to surface distributions and anomalies visually.

Input data intentionally contains common real-world entry problems:

- Blank rows and fully empty records
- Mixed date formats (`DD/MM/YYYY`, `YYYY-MM-DD`, `DD/MM/YY`)
- Inconsistent unit labels for the same measurement (`kwh`, `kWh`, `KWh`, `kilowattora`)
- Mixed casing and abbreviations in category names (`ENERGIA`, `energia elettrica`, `Riscald.`)
- Pseudo-null strings (`N/D`, `-`, `?`, `da definire`) instead of actual `NaN`

### Phase 2 — Data Cleaning & Standardisation

Each file goes through a multi-step cleaning pipeline before merging:

- **Column normalisation** — headers are stripped and title-cased to prevent misalignment on concatenation
- **Text standardisation** — categories, resource names, and units are mapped to canonical forms via lookup dictionaries defined in `config.py`
- **Pseudo-null replacement** — non-standard missing value strings are replaced with `NaN`
- **Missing value inference** — where `Categoria` is missing but `Risorsa` uniquely determines it, the value is filled automatically
- **Invalid quantity removal** — rows with `Quantità ≤ 0` are dropped
- **Unit validation** — rows where the recorded unit does not match the expected unit for that resource are removed
- **Duplicate removal** — exact duplicate rows are dropped
- **Date parsing** — all date format variants are parsed to a consistent `date` type using `pd.to_datetime(format='mixed', dayfirst=True)`

After cleaning, the three DataFrames are concatenated with an `Impianto` tracking column into a single master DataFrame.

**Outlier removal (IQR method):** Per-resource boxplots are used as a visual diagnostic, followed by IQR-based removal (threshold 1.5×) for four resources: `Gas Naturale`, `Elettricità`, `Gas refrigerante R410A`, and `Benzina`. `Rifiuti speciali` is explicitly excluded — its high values are operationally plausible and not attributable to data entry errors. This distinction between a statistical outlier and a genuine extreme value is documented in the notebook.

### Phase 3 — GHG Emission Quantification

Emission factors are applied record by record to compute `kgCO₂e`:

```
Emissions (kgCO₂e) = Quantity × Emission Factor
```

Factors are centralised in `config.py` and sourced from established regulatory references:

| Resource | Factor | Unit | Source |
|---|---|---|---|
| Natural Gas | 0.202 | kgCO₂e / m³ | GHG Protocol / DEFRA 2024 |
| Diesel | 0.267 | kgCO₂e / litre | GHG Protocol / DEFRA 2024 |
| Petrol | 0.249 | kgCO₂e / litre | GHG Protocol / DEFRA 2024 |
| Biomass | 0.0 | kgCO₂e / kg | ISPRA (carbon-neutral convention) |
| Refrigerant R410A | 2088.0 | kgCO₂e / kg | GWP100, IPCC AR5 |
| Water supply | 0.149 | kgCO₂e / m³ | DEFRA 2024 |
| Special waste | 0.616 | kgCO₂e / kg | DEFRA 2024 |
| Municipal waste | 0.467 | kgCO₂e / kg | DEFRA 2024 |
| Electricity — IT (Milano, Roma) | 0.233 | kgCO₂e / kWh | ISPRA 2023 |
| Electricity — FR (Lione) | 0.052 | kgCO₂e / kWh | ADEME / RTE 2022–2024 |

Electricity uses location-based factors split by city: the French grid (dominated by nuclear) is roughly 4.5× cleaner than the Italian mix, so applying a single national factor would significantly misrepresent Lione's footprint.

The resources in this dataset span **Scope 1** (direct combustion and fugitive refrigerant emissions), **Scope 2** (purchased electricity), and elements commonly reported alongside **Scope 3** (water, waste).

### Phase 4 — Audit-Ready Excel Export

A formatted multi-sheet workbook is generated using `pandas` for data writing and `openpyxl` for formatting:

| Sheet | Content |
|---|---|
| `Sintesi_Globale` | Pivot table: total kgCO₂e by facility × category × year, with grand totals |
| `Sintesi_Milano` | Same pivot, Milano only |
| `Sintesi_Lione` | Same pivot, Lione only |
| `Sintesi_Roma` | Same pivot, Roma only |
| `Dettaglio_emissioni` | Full row-level audit trail with emission factors and calculated values |

The detail sheet ensures full traceability — every number in the summary tabs can be traced back to a specific consumption record. Formatting includes auto-fitted column widths, `#,##0.00` number format, `DD/MM/YYYY` date format, alignment by column type, and bold styling for total rows and columns.


## Tech Stack

- **Python 3.x**
- **pandas** — data loading, cleaning, transformation, pivot tables
- **numpy** — null replacement and numerical operations
- **openpyxl** — Excel formatting
- **matplotlib** — boxplot visualisations for outlier analysis
- **sweetviz** — automated EDA reports


## Possible Extensions

A few directions this pipeline could be expanded in the future:

**Anomaly detection layer.** Before calculating emissions, a validation step could flag any consumption record that deviates significantly from a facility's historical moving average (e.g. >50% above the trailing 12-month mean). Anomalous rows would be isolated in an `error_log.txt` for manual review rather than silently dropped or included.

**Live emission factor API.** The static dictionaries in `config.py` could be replaced with real-time queries to a carbon intelligence API such as [Climatiq](https://www.climatiq.io/), which provides country-specific and year-specific factors updated continuously. This would eliminate the need to manually update the config file each year.

**Interactive Streamlit dashboard.** The static Excel report could be complemented with a browser-based interface built in `Streamlit`, allowing non-technical stakeholders to upload facility files directly and explore emission breakdowns through interactive charts — without needing to run the notebook.
