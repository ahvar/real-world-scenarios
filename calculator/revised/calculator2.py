from collections import defaultdict

plans = defaultdict(list)
with open("../data/plans.csv", "r") as plans_in:
    plans_header = next(plans_in)
    for line in plans_in:
        plan_id, state, metal_level, rate, rate_area = line.strip().split(",")
        plans[rate_area].append((plan_id, state, metal_level, rate))

slcsp = defaultdict(list)
with open("../data/slcsp.csv", "r") as slcsp_in:
    slcsp_header = next(slcsp_in)
    for line in slcsp_in:
        zipcode = line.strip()
        slcsp[zipcode] = []

zips = defaultdict(list)
with open("../data/zips.csv", "r") as zips_in:
    zips_header = next(zips_in)
    for line in zips_in:
        zipcode, state, cc, name, rate_area = line.strip().split(",")
        zips[zipcode].append((state, cc, name, rate_area))

output = []
for zipcode in slcsp:
    # 1. find the (state, rate_area) for this zip code
    rate_areas = set(
        (state, rate_area) for state, cc, name, rate_area in zips.get(zipcode, [])
    )
    if len(rate_areas) != 1:
        output.append((zipcode, ""))
        continue
    # 2. find all the silver plans for this rate area
    state, rate_area = next(iter(rate_areas))
    silver_rates = set(
        float(rate)
        for plan_id, p_state, metal_level, rate in plans[rate_area]
        if metal_level == "Silver"
    )
    if len(silver_rates) < 2:
        output.append(zipcode, "")
    else:
        sorted_rates = sorted(silver_rates)
        output.append((zipcode, f"{sorted_rates[1]:.2f}"))
