from statistics import mean

def calculate_best_fit_slope(xs, ys):
    multArray = []
    for i in range(len(xs)):
        multArray += [xs[i]*ys[i]]
    multArray2 = []
    for i in range(len(xs)):
        multArray2 += [xs[i]*xs[i]]
    m = (((mean(xs)*mean(ys)) - mean(multArray)) / ((mean(xs)*mean(xs)) - mean(multArray2)))
    return m

def get_weight_rate(entries):
    xs = []
    ys = []
    for i in range(len(entries)):
        if entries[i] != None and "weight" in entries[i]:
            xs.append(i)
            ys.append(entries[i]["weight"])
    return calculate_best_fit_slope(xs, ys)

def get_body_fat_rate(entries):
    xs = []
    ys = []
    for i in range(len(entries)):
        if entries[i] != None and "body_fat" in entries[i]:
            xs.append(i)
            ys.append(entries[i]["body_fat"])
    return calculate_best_fit_slope(xs, ys)