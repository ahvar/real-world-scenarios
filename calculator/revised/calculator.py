import json
import csv


plans = {}
with open("../data/plans.csv", "r") as plans_in:
    reader = csv.DictReader(plans_in)
    for line in reader:
        rate_area = line["rate_area"]
        if line["rate_area"] not in plans:
            plans[rate_area] = [
                {
                    "rate": line["rate"],
                    "metal_level": line["metal_level"],
                    "state": line["state"],
                    "plan_id": line["plan_id"],
                }
            ]
        else:
            plans[rate_area].append(
                {
                    "rate": line["rate"],
                    "metal_level": line["metal_level"],
                    "state": line["state"],
                    "plan_id": line["plan_id"],
                }
            )

slcsp = {}
with open("../data/slcsp.csv", "r") as slcsp_in:
    reader = csv.reader(slcsp_in)
    zip_header = next(reader)
    for line in reader:
        slcsp[line[0]] = []

zips = {}
with open("../data/zips.csv", "r") as zips_in:
    reader = csv.DictReader(zips_in)
    for line in reader:
        zipcode = line["zipcode"]
        if zipcode not in zips:
            zips[zipcode] = [
                {
                    "name": line["name"],
                    "county_code": line["county_code"],
                    "state": line["state"],
                    "rate_area": line["rate_area"],
                }
            ]
        else:
            zips[zipcode].append(
                {
                    "name": line["name"],
                    "county_code": line["county_code"],
                    "state": line["state"],
                    "rate_area": line["rate_area"],
                }
            )


for zipcode, data in zips.items():
    if len(data) > 1:
        rate_areas = [d["rate_area"] for d in data]
        # is there more than one rate area per zipcode
        if len(set(rate_areas)) > 1:
            slcsp[zipcode] = ""
        else:
            slcsp[zipcode] = rate_areas[0]
    else:
        slcsp[zipcode] = data[0]["rate_area"]


# print(json.dumps(slcsp, indent=4))
print("zipcde, rate_area, slcsp")
for zipcode, rate_area in slcsp.items():
    for plan_rate_area, plan_data in plans.items():
        if plan_rate_area == rate_area:
            rates = [
                data["rate"] for data in plan_data if data["metal_level"] == "Silver"
            ]
            if len(rates) < 2:
                continue
            rates.sort()
            print(zipcode, rate_area, rates[1])
