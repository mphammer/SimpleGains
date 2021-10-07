import json

def read_json(filepath="_simplegains.json"):
    with open(filepath) as json_file:
        data = json.load(json_file)
    return data

def write_json(data, filepath="_simplegains.json"):
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)

def get_setup_values():
    # Collect Inputs For Calculating TDEE
    age_years = input("Age (years): ")
    height_inches = input("Height (inches): ")
    weight_lbs = input("Weight (lbs): ")
    bfp = input("Body Fat Percentage: ")
    activity_hours = input("Estimated Hours Of Weekly Activity: ")

    # Create weight_log.txt file
    f = open("weight_log.txt", "w")
    f.write("<date MM-dd-yyyy> <weight_lbs> <body fat percent>\n")
    f.close()

    data = {
        "age_years": float(age_years),
        "height_inches": float(height_inches),
        "weight_lbs": float(weight_lbs),
        "bfp": float(bfp),
        "activity_hours": float(activity_hours)
    }

    write_json(data)

if __name__ == "__main__":
    get_setup_values()