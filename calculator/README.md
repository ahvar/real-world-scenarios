# SLCSP Calculator Guide

This project calculates the **Second Lowest Cost Silver Plan (SLCSP)** premium for the ZIP codes listed in the input dataset.

## Overview
The `slcsp_calc.py` script determines the monthly premium associated with the second cheapest silver-tier health insurance plan available within the appropriate geographic rating area. The calculation relies on data sourced from three CSV inputs:

- **`slcsp.csv`** – ZIP codes for which the SLCSP must be reported. The output mirrors this file with an additional column containing the SLCSP rate (or blank when indeterminable).
- **`plans.csv`** – A catalog of available health insurance plans, including their metal level, monthly premium, and the rate areas they serve.
- **`zips.csv`** – A mapping from ZIP codes to county/state combinations used to derive each unique rate area.

## Algorithm
1. **Parse and structure data** – Load the CSV files into convenient in-memory structures (e.g., dictionaries, dataframes) that support efficient lookup.
2. **Map ZIP codes to rate areas** – Determine the rate area for each ZIP code in `slcsp.csv` using `zips.csv`.
   - If a ZIP code spans multiple rate areas, the SLCSP cannot be uniquely determined and should remain blank.
3. **Filter eligible plans** – Identify plans that:
   - Are classified at the **Silver** metal level.
   - Are offered in the relevant rate area.
4. **Select the second-lowest rate** – Collect the unique premium values from the qualifying silver plans, sort them in ascending order, and choose the second entry. This is the SLCSP premium for that rate area.
5. **Handle edge cases** – If a rate area has fewer than two unique silver plan premiums, the SLCSP is undefined and must be left blank in the output.
6. **Consider Essential Health Benefits (EHBs)** – If plan data includes services beyond EHBs (e.g., adult dental), only the EHB portion of the premium applies to the SLCSP computation.
7. **Generate output** – Write the results to stdout, reproducing `slcsp.csv` with the calculated premium values (or blanks) appended.

## Usage
1. Ensure the required CSV files (`slcsp.csv`, `plans.csv`, and `zips.csv`) are available.
2. Run the script, directing output to a file if desired:
   ```bash
   python slcsp_calc.py slcsp.csv plans.csv zips.csv > results.csv
   ```
3. Review `results.csv` for the SLCSP premiums corresponding to each ZIP code.

## Notes
- Always verify that the ZIP-to-rate area mapping is unambiguous before reporting an SLCSP value.
- Maintain clean, structured data to avoid discrepancies during filtering and sorting operations.
- Update this README if additional data requirements or processing steps are introduced.
