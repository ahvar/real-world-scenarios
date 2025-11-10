import json
import csv


plans = {}
with open("../data/plans.csv", "r") as plans_in:
    reader = csv.DictReader(plans_in)
    for line in reader:
        rate_area = line["rate_area"]
        if line["rate_area"] not in plans:
            plans[rate_area] = {
                "rates": [line["rate"]],
                "metal_level": [line["metal_level"]],
                "states": [line["state"]],
                "plan_ids": [line["plan_id"]],
            }
        else:
            plans[rate_area]["rates"].append(line["rate"])
            plans[rate_area]["metal_level"].append(line["metal_level"])
            plans[rate_area]["states"].append(line["state"])
            plans[rate_area]["plan_ids"].append(line["plan_id"])

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
        rate_area = line["rate_area"]
        if rate_area not in zips:
            zips[rate_area] = {
                "name": [line["name"]],
                "county_code": [line["county_code"]],
                "state": [line["state"]],
                "zipcode": [line["zipcode"]],
            }
        else:
            zips[rate_area]["name"].append(line["name"])
            zips[rate_area]["county_code"].append(line["county_code"])
            zips[rate_area]["state"].append(line["state"])
            zips[rate_area]["zipcode"].append(line["zipcode"])


for rate_area, data in zips.items():
    zipcode = zips[rate_area]["zipcode"]
    if set(zips[rate_area][zipcode]) > 1:
        slcsp[zipcode].append("")
    else:
        slcsp[zipcode].append({"rate_area": rate_area, "zipcode": zipcode})
