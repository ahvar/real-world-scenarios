

## Algorithm
1. **Parse plans**
 - There are many plan Ids, metal levels, and rates per rate area so read those data into
 a dict with rate area as the keys and plan ids, metal levels, rates, and states as the values. Each line of data in the plans file represents data for one plan id, so put the plan id, metal level, rate, and state in a dict and store that dict in a list
2. **Read slcsp** – Store each zip code in slcsp in a dict with zips as keys and values as empty lists to be populated later.

3. **Read zips** - Read zipcodes into a dict with zipcodes as keys and each value being a list of dicts with each dict representing a line in the zipcode file. A zipcode can have different rate areas across multiple counties or states, and in this case the slcsp for that zip cannot be determined. 

3. **Filter eligible plans** – Identify plans that:
   - Are classified at the **Silver** metal level.
   - Are offered in the relevant rate area.
4. **Select the second-lowest rate** – Collect the unique premium values from the qualifying silver plans, sort them in ascending order, and choose the second entry. This is the SLCSP premium for that rate area.
5. **Handle edge cases** – If a rate area has fewer than two unique silver plan premiums, the SLCSP is undefined and must be left blank in the output.
6. **Consider Essential Health Benefits (EHBs)** – If plan data includes services beyond EHBs (e.g., adult dental), only the EHB portion of the premium applies to the SLCSP computation.
7. **Generate output** – Write the results to stdout, reproducing `slcsp.csv` with the calculated premium values (or blanks) appended.