import csv
import json


def get_rate_area_by_zip():
    zips = {}
    with open("../data/zips.csv", "r") as zips_file:
        reader = csv.reader(zips_file)
        headers = next(reader)
        for row in reader:
            code, state, county, name, rate_area = row
            if code in zips:
                zips[code] = ""
            else:
                zips[code] = {
                    "rate_area": rate_area,
                    "county": county,
                    "name": name,
                    "state": state,
                }
    return zips, headers


def find_second_lowest_silver_plans(merged):
    slcsp = {}
    with open("../data/plans.csv", "r") as plans_file:
        reader = csv.reader(plans_file)
        plans_header = next(reader)
        for row in reader:
            plan_id, state, metal_level, rate, rate_area = row
            if metal_level == "Silver":
                if rate_area in slcsp:
                    slcsp[rate_area].append(rate)
                else:
                    slcsp[rate_area] = [rate]
    second_lowest = {}
    for area, rates in slcsp.items():
        rates.sort()
        if len(rates) > 1:
            rates.sort()
            second_lowest[area] = rates[1]
        else:
            second_lowest[area] = rates[0]

    for zip, zipdata in merged.items():
        for area, cost in second_lowest.items():
            if area == zipdata["rate_area"]:
                zipdata["second_lowest"] = cost
                print(zipdata)
    # print(json.dumps(merged, indent=4))
    # print(json.dumps(second_lowest, indent=4))


def get_slcsp_zips():
    slcsp = {}
    with open("../data/slcsp.csv", "r") as slcsp_file:
        reader = csv.DictReader(slcsp_file)
        slcsp_header = next(reader)
        for row in reader:
            zipcode = row["zipcode"]
            slcsp[zipcode] = ""
    return slcsp, slcsp_header


if __name__ == "__main__":
    zips_with_rates, zip_headers = get_rate_area_by_zip()
    slcsp_zips, slcsp_header = get_slcsp_zips()
    # print("Rate Areas by Zip Code")
    # print(json.dumps(zips_with_rates, indent=4))
    # print("SLCSP Zip Codes")
    # print(json.dumps(slcsp_zips, indent=4))

    merged = {**slcsp_zips, **zips_with_rates}
    find_second_lowest_silver_plans(merged)
    # read all plan data
    # add the second lowest rate silver plan to the merged dataset
