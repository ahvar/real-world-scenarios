from pathlib import Path
from collections import defaultdict

zip_code_file = Path(__file__).parent.parent / "data" / "zips.csv"
slcsp_zip_code_file = Path(__file__).parent.parent / "data" / "slcsp.csv"
plans_file = Path(__file__).parent.parent / "plans.csv"

plan_rates = defaultdict(list)
with open(plans_file, "r") as plans_in:
    header = next(plans_in)
    for line in plans_in:
        plan_id, state, metal_level, rate, rate_area = line.strip().split(",")
        if metal_level.lower() == "silver":
            plan_rates[(state, rate_area)].append(float(rate))

slcsp_zip_data = []
with open(slcsp_zip_code_file, "r") as slcsp_in:
    header = next(slcsp_in)
    for line in slcsp_in:
        zipcode = line.strip().split()[0]
        slcsp_zip_data.append(zipcode)


rate_area_zipcode = defaultdict(set)
with open(zip_code_file, "r") as ra_zip_in:
    header = next(ra_zip_in)
    for line in ra_zip_in:
        zipcode, state, county, cc, name, rate_area = line.strip().split(",")
        rate_area_zipcode[zipcode].add((state, rate_area))

output = []
for zipcode in slcsp_zip_data:
    rate_areas = rate_area_zipcode.get(zipcode, set())
    if len(rate_areas) != 1:
        output.append((zipcode, ""))
        continue
    state, rate_area = next(iter(rate_areas))
    slcsp = sorted(set(plan_rates.get((state, rate_area), [])))
    if len(slcsp) < 2:
        output.append((zipcode, ""))
    else:
        output.append((zipcode, float(f"{slcsp:2f}")))
