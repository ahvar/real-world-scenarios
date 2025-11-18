import json
from pathlib import Path

plans_path = Path("../data/plans.csv")
zips_path = Path("../data/zips.csv")
slcsp = Path("../data/slcsp.csv")

plan_data = {}
with plans_path.open() as plans_in:
    plans_headers = next(plans_in)
    for line in plans_in:
        id, state, metal, rate, area = line.strip().split(",")
        plan_data.setdefault(area, []).append(
            {"id": id, "state": state, "metal": metal, "rate": rate, "area": area}
        )

zips_data = {}
with zips_path.open() as zips_in:
    zips_headers = next(zips_in)
    for line in zips_in:
        zip, state, code, name, area = line.strip().split(",")
        zips_data.setdefault(zip, []).append(
            {"zip": zip, "state": state, "code": code, "name": name, "area": area}
        )


zips_data = {
    zip: data
    for zip, data in zips_data.items()
    if len(set(record["area"] for record in data)) == 1
}

slcsp_data = {}
with slcsp.open() as slcsp_in:
    slcsp_headers = next(slcsp_in)
    for line in slcsp_in:
        zip = line.strip()
        slcsp_data.setdefault(zip, [])
