import csv
import json

plans = []
zips = []
slcsp = []
with open("../data/plans.csv", "r") as plans_file:
    reader = csv.DictReader(plans_file)
    for row in reader:
        plans.append(
            {
                "plan_id": row["plan_id"],
                "state": row["state"],
                "metal_level": row["metal_level"],
                "rate": row["rate"],
                "rate_area": row["rate_area"],
            }
        )

with open("../data/zips.csv", "r") as zips_file:
    reader = csv.DictReader(zips_file)
    for row in reader:
        zips.append(
            {
                "zipcode": row["zipcode"],
                "state": row["state"],
                "county_code": row["county_code"],
                "name": row["name"],
                "rate_area": row["rate_area"],
            }
        )
with open("../data/slcsp.csv", "r") as slcsp_file:
    zipcode = slcsp_file.readline().strip()
    slcsp.append({"zipcode": zipcode})

seen = []
overlap = []
for zip_data in zips:
    if zip_data["zipcode"] in seen:
        overlap.append(zip_data["zipcode"])

for zip_data in slcsp:
    if zip_data["zipcode"] in overlap:
        zip_data["slcsp_rate"] = ""


"""
 slcsp_rate_areas = []
zip_count = 0
for slcsp_zip_code in slcsp:
    zips = [ zip_count += 1 for zip_data in zips if slcsp_zip_code['zipcode'] == zip_data['zipcode'] ]
 
"""
