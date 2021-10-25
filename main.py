from datetime import datetime, timedelta
from _best_fit_slope import *
from _markdown_file import *
from setup_script import *
from _body_composition_calculator import *
import matplotlib.pyplot as plt
import numpy as np

def read_weight_log(log_path="weight_log.txt"):
    weight_log = {}
    with open(log_path) as file: 
        for line in file: 
            split_line = line.split(" ")
            date_str = split_line[0]
            weight_lbs = float(split_line[1])
            bfp = float(split_line[2])
            weight_log[date_str] = {
                "weight_lbs": weight_lbs,
                "bfp": bfp
            }
    return weight_log

def str_to_datetime(date_str, date_format="%m-%d-%Y"):
    return datetime.strptime(date_str, date_format)

def datetime_to_str(datetime_obj, date_format="%m-%d-%Y"):
    return datetime_obj.strftime(date_format)

def datetime_to_prev_day(datetime_obj):
    return datetime_obj - datetime.timedelta(days=1)

def get_last_N_logs(weight_log, n):
    logs = {}
    curr_date = datetime.today()
    for i in range(n):
        date_str = datetime_to_str(curr_date)
        if date_str in weight_log:
            logs[date_str] = weight_log[date_str]
        curr_date -= timedelta(days=1)
    return logs

def get_last_N_weight_points(weight_log, n):
    points = []
    curr_date = datetime.today()
    for i in range(n):
        date_str = datetime_to_str(curr_date)
        if date_str in weight_log:
            points.append(weight_log[date_str]["weight_lbs"])
        else: 
            points.append(0.0)
        curr_date -= timedelta(days=1)
    points.reverse()
    return points

def get_last_N_bfp_points(weight_log, n):
    points = []
    curr_date = datetime.today()
    for i in range(n):
        date_str = datetime_to_str(curr_date)
        if date_str in weight_log:
            points.append(weight_log[date_str]["bfp"])
        else: 
            points.append(0.0)
        curr_date -= timedelta(days=1)
    points.reverse()
    return points

def get_X_values_from_data_values(weight_values):
    points = []
    count = 0
    for pt in weight_values:
        if pt != 0.0:
            points.append(count)
        count += 1
    return points


def get_avg_weight(weight_log):
    weight_sum = 0
    weight_count = 0
    for date_str, data in weight_log.items():
        weight_sum += data["weight_lbs"]
        weight_count += 1
    if weight_count == 0.0:
        return 0.0
    return weight_sum / weight_count

def get_avg_bfp(weight_log):
    bfp_sum = 0
    bfp_count = 0
    for date_str, data in weight_log.items():
        bfp_sum += data["bfp"]
        bfp_count += 1
    if bfp_count == 0.0:
        return 0.0
    return bfp_sum / bfp_count

def calc_calories_for_goal_rate(curr_lbs_per_week, goal_lbs_per_week=0.75):
    cals_in_lb = 3500.0
    curr_cals_over_per_week = curr_lbs_per_week * cals_in_lb
    goal_cals_over_per_week = goal_lbs_per_week * cals_in_lb

    curr_cals_over_per_day = curr_cals_over_per_week / 7.0
    goal_cals_over_per_day = goal_cals_over_per_week / 7.0

    return goal_cals_over_per_day - curr_cals_over_per_day


if __name__ == "__main__":
    # Read in the weight log
    body_comp_data = read_json()
    weight_log = read_weight_log()

    results_file = MarkdownFile()

    bmr = calculate_BMR(body_comp_data["weight_lbs"], body_comp_data["height_inches"], body_comp_data["age_years"])
    tdee = get_average_weekly_TDEE(bmr, body_comp_data["activity_hours"])
    results_file.write_text("STATS: Age {}; Weight {}; Height {}; Exercise Hours {}".format(body_comp_data["age_years"], body_comp_data["weight_lbs"], body_comp_data["height_inches"], body_comp_data["activity_hours"]))
    results_file.write_text("Estimated TDEE: {:.2f}".format(tdee))
    results_file.write_line()

    data = {}
    weeks = range(1,6)
    days_in_week = 7
    for i in weeks:
        week_logs = get_last_N_logs(weight_log, i*days_in_week)
        data["week_logs"] = week_logs
        data["avg_weight"] = get_avg_weight(data["week_logs"])
        data["avg_bfp"] = get_avg_bfp(data["week_logs"])
        # weight
        data["weight_values"] = get_last_N_weight_points(weight_log, i*days_in_week)
        data["weight_x_points"] = get_X_values_from_data_values(data["weight_values"])
        data["weight_y_points"] = [x for x in data["weight_values"] if x != 0.0]
        data["weight_best_fit_slope"] = calculate_best_fit_slope(data["weight_x_points"], data["weight_y_points"])
        # bfp
        data["bfp_values"] = get_last_N_bfp_points(weight_log, i*days_in_week)
        data["bfp_x_points"] = get_X_values_from_data_values(data["bfp_values"])
        data["bfp_y_points"] = [x for x in data["bfp_values"] if x != 0.0]
        data["bfp_best_fit_slope"] = calculate_best_fit_slope(data["bfp_x_points"], data["bfp_y_points"])

        plt.plot(data["weight_x_points"], data["weight_y_points"])
        z = np.polyfit(data["bfp_x_points"], data["weight_y_points"], 1)
        p = np.poly1d(z)
        plt.plot(data["weight_x_points"],p(data["weight_x_points"]),"r--", linewidth=1)
        plot_name = 'data/week-{}-weight-trend.png'.format(i)
        plt.savefig(plot_name)
        plt.clf()

        goal_bulk_rate = 0.5
        goal_cut_rate = -0.75
        bulk_cal_adjustment = calc_calories_for_goal_rate(data["weight_best_fit_slope"], goal_bulk_rate)
        cut_cal_adjustment = calc_calories_for_goal_rate(data["weight_best_fit_slope"], goal_cut_rate)

        results_file.write_heading("Results Over Past {} Week(s)".format(i))
        results_file.write_image(plot_name)
        results_file.write_text("Rates: Weight {:.2f} lbs/week; Bfp {:.2f} %/week".format(data["weight_best_fit_slope"]*days_in_week, data["bfp_best_fit_slope"]*days_in_week))
        results_file.write_text("Averages: Weight {:.2f} lbs; Bfp {:.2f}%".format(data["avg_weight"], data["avg_bfp"]))
        results_file.write_text("To bulk at {:.2f} lbs/week you should adjust daily calories by {:.2f}".format(goal_bulk_rate, bulk_cal_adjustment))
        results_file.write_text("To cut at {:.2f} lbs/week you should adjust daily calories by {:.2f}".format(goal_cut_rate, cut_cal_adjustment))
        
        max_bfp = 13.0
        min_bfp = 10.0
        if data["avg_bfp"] >= max_bfp:
            results_file.write_text("Your body fat percentage is above {}%. You should cut.".format(max_bfp))
        elif data["avg_bfp"] <= min_bfp:
            results_file.write_text("Your body fat percentage is above {}%. You should bulk.".format(min_bfp))
        else:
            results_file.write_text("Your body fat percentage is within {}-{}%. Keep going!".format(min_bfp, max_bfp))
    