from collections import defaultdict

plans = defaultdict()
with open("../data/plans.csv") as plans_in:
    plan_headers = next(plans_in)
    for line in plans_in:
        plan_id, state, metal_level, rate, rate_area = line
        if rate_area in plans:
            plans[rate_area].append(
                {
                    "plan_id": plan_id,
                    "state": state,
                    "metal_level": metal_level,
                    "rate": rate,
                }
            )
        else:
            plans[rate_area] = [
                {
                    "plan_id": plan_id,
                    "state": state,
                    "metal_level": metal_level,
                    "rate": rate,
                }
            ]

slcsp = defaultdict()
with open("../data/slcsp.csv") as slcsp_in:
    slcsp_headers = next(slcsp_in)
    for line in slcsp_in:
        zip = line.read()
        slcsp[zip] = []

zips = defaultdict()
with open("../data/zips.csv") as zips_in:
    zips_headers = next(zips_in)
    for line in zips_in:
        zip, state, cc, name, rate_area = line
        if zip in zips:
            zips[zip].append(
                {
                    "zip": zip,
                    "state": state,
                    "cc": cc,
                    "name": name,
                    "rate_area": rate_area,
                }
            )
        else:
            zips[zip] = [
                {
                    "zip": zip,
                    "state": state,
                    "cc": cc,
                    "name": name,
                    "rate_area": rate_area,
                }
            ]
