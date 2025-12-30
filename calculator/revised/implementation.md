

## Algorithm
1. **Parse plans**
 - Read plans.csv into dict with a state, rate_area tuple as key and the rate as value. Store the value as a float. Keep only Silver plans
2. **Read slcsp** – Read slcsp.csv data into a list; preserve order
3. **Read zips** - Read zips.csv into a dict with zipcode as keys and sets of state, rate area tuple as the values
4. **Filter eligible plans** – Iterate slcsp zipcodes. For each zipcode, get the corresponding state and rate area from the dict storing those values by zipcode. If there are 0 or more than 1 rate areas for a zipcode, append an empty string for that zipcode to the output array. Unpack the state and rate area
4. **Select the second-lowest rate** – Use the state and rate area to get the rates from the plan dictionary that has rates by state and rate area
5. **Handle edge cases** – If the length of the returned rates is less than 2, then it means there was more than one rate area for a zipcode and there for the slcsp for that rate area could not be determined.
6. **Consider Essential Health Benefits (EHBs)** – If plan data includes services beyond EHBs (e.g., adult dental), only the EHB portion of the premium applies to the SLCSP computation.
7. **Generate output** – Write the results to stdout, reproducing `slcsp.csv` with the calculated premium values (or blanks) appended.