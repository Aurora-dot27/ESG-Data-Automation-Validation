# Automated Corporate Sustainability & GHG Accounting Pipeline

This repository contains a professional-grade development sandbox that simulates the end-to-end data pipeline of a corporate sustainability analyst or ESG consultant. It serves as a practical demonstration of scalable data engineering practices applied to environmental compliance and carbon accounting. 

The core objective of this project is to automate the ingestion, cleaning, and standardization of fragmented, non-standardized facility-level consumption data, compute audited corporate greenhouse gas (GHG) footprints (Scope 1 & Scope 2), and generate financial-grade, structured reporting assets ready for sustainability disclosures.

---

## Data Pipeline Architecture

The pipeline processes messy, multi-facility raw data through a standardized three-tier ETL (Extract, Transform, Load) architecture implemented in Python.

### 1. Data Ingestion & Inconsistent Input Management
The pipeline simulates a realistic corporate environment where data is received from separate, decoupled operational facilities (e.g., `consumi_milano.xlsx`, `consumi_lione.xlsx`). Input data intentionally contains common human-entry anomalies to test pipeline resilience:
* **Structural Flaws:** Missing records, blank rows, and unformatted data blocks.
* **Temporal Inconsistencies:** Divergent datetime formats (e.g., mixing `DD/MM/YYYY` with `YYYY-MM-DD`).
* **Categorical Discrepancies:** Mixed casing and non-standardized units of measurement for identical metrics (e.g., `kwh`, `kWh`, `KWh`).

### 2. Core Python Processing Module
* **Extraction & Standardization (`pandas`):** Consolidates isolated multi-facility ledgers into a single, cohesive enterprise-wide DataFrame. The ingestion engine programmatically enforces lower-case string normalization, drops null rows missing critical quantitative values, and resolves temporal schema mutations into a unified datetime index.
* **GHG Emission Quantification (ESG Logic):** Maps consumption data against an integrated database of localized, regulatory emission factors (e.g., ISPRA for Italian grid electricity, DEFRA for stationary combustion fuels). The computation engine isolates active variables, applies the respective multipliers, and appends a computed `Emissioni_kgCO2e` attribute across thousands of transactions deterministically.

### 3. Audit-Ready Financial Export (`openpyxl` / `xlsxwriter`)
Rather than outputting raw, flat CSV strings, the pipeline generates a highly formatted, multi-tab executive asset named `Report_Emissioni_2026.xlsx`:
* **`Sintesi` (Executive Summary Tab):** An automated programmatic pivot table aggregation illustrating total emissions cross-referenced by specific Facility and GHG Protocol Scope (Scope 1 for direct fuel combustion, Scope 2 for indirect purchased electricity).
* **`Dati Puliti` (Granular Audit Trail Tab):** The complete, standardized transaction ledger with embedded localized emission factors and calculated carbon values, ensuring full traceability for external assurance auditors.

---

## Roadmap & Future Enhancements

To expand the scalability and sophistication of this environment, the following modules are currently under active development:

### Milestone A: Data Quality Assurance & Anomaly Detection
* **Objective:** Implement an automated input-validation layer to mitigate human reporting errors prior to calculation.
* **Mechanism:** A statistical threshold engine evaluating rolling facility historical consumption. If a newly ingested monthly metric deviates by over +50% from the facility's historical moving average, the pipeline halts execution for that row and isolates the anomaly inside a dedicated `error_log.txt` asset for manual data-assurance remediation.

### Milestone B: External ESG API Integration
* **Objective:** Replace static internal coefficient dictionaries with live, real-time external data queries.
* **Mechanism:** Refactor the calculation engine to connect directly to external carbon intelligence APIs (e.g., Climatiq). This enables dynamic retrieval of dynamically adjusted, country-specific, and year-specific emission factors programmatically via authenticated HTTPS requests.

### Milestone C: Interactive Analytical Dashboard
* **Objective:** Transition the reporting layer from static spreadsheets to dynamic, interactive management reporting utilities.
* **Mechanism:** Build a localized browser-based interface using `Streamlit`. This application layer will allow non-technical stakeholder executives to upload raw facility spreadsheets via a drag-and-drop UI and instantly render interactive data visualizations (e.g., programmatic categorical pie charts, temporal trend bars) showing enterprise-level carbon intensity.

---

## Technology Stack

* **Language:** Python 3.10+
* **Data Manipulation:** Pandas
* **Spreadsheet Engineering:** Openpyxl / Xlsxwriter
* **Environment Management:** Virtualenv / Pipenv
