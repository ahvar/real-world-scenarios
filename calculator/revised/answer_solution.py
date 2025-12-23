from collections import defaultdict

# 1. Parse plans.csv into a dict by rate_area, only keeping the Silver plans
plans_by_rate_area = defaultdict(list)
with open("../data/plans.csv", "r") as plans_in:
    plans_header = next(plans_in)
    for line in plans_in:
        plan_id, state, metal_level, rate, rate_area = line.strip().split(",")
        if metal_level == "Silver":
            plans_by_rate_area[(state, rate_area)].append(float(rate))

# 2. Read slcsp.csv and store zipcodes in a list to preserve order
zipcodes = []
with open("../data/slcsp.csv", "r") as slcsp_in:
    slcsp_header = next(slcsp_in)
    for line in slcsp_in:
        zipcode = line.strip().split(",")[0]
        zipcodes.append(zipcode)

# 3. Read zips.csv and map zipcodes to all (state, rate_area) pairs
zips_to_rate_areas = defaultdict(set)
with open("../data/zips.csv", "r") as zips_in:
    zips_header = next(zips_in)
    for line in zips_in:
        zipcode, state, cc, name, rate_area = line.strip().split(",")
        zips_to_rate_areas[zipcode].add((state, rate_area))

output = []
for zipcode in zipcodes:
    rate_areas = zips_to_rate_areas.get(zipcode, set())
    if len(rate_areas) != 1:
        output.append((zipcode, ""))
        continue
    state, rate_area = next(iter(rate_areas))  # not possible to unpack rate_areas?
    rates = sorted(set(plans_by_rate_area.get((state, rate_area), [])))
    if len(rates) < 2:
        output.append((zipcode, ""))
    else:
        output.append((zipcode, f"{rates[1]:.2f}"))

import sys

print("zipcode, rate")
for zipcode, rate in output:
    print(f"{zipcode}, {rate}")
