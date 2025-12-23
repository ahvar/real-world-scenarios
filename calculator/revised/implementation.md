

## Algorithm
1. **Parse plans**
 - Read plans.csv into dict by state, rate_area; keep only Silver plans
2. **Read slcsp** – Read slcsp.csv data into a list; preserve order

3. **Read zips** - Read zips.csv and map zipcodes to all (state, rate_area) pairs

3. **Filter eligible plans** – Identify plans that:
   - Are classified at the **Silver** metal level.
   - Are offered in the relevant rate area.
4. **Select the second-lowest rate** – Collect the unique premium values from the qualifying silver plans, sort them in ascending order, and choose the second entry. This is the SLCSP premium for that rate area.
5. **Handle edge cases** – If a rate area has fewer than two unique silver plan premiums, the SLCSP is undefined and must be left blank in the output.
6. **Consider Essential Health Benefits (EHBs)** – If plan data includes services beyond EHBs (e.g., adult dental), only the EHB portion of the premium applies to the SLCSP computation.
7. **Generate output** – Write the results to stdout, reproducing `slcsp.csv` with the calculated premium values (or blanks) appended.